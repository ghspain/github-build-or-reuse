#!/usr/bin/env python3
"""Validate sanitized cross-client behavioral evidence for github-build-or-reuse."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE_DIR = ROOT / "evidence" / "behavioral"
CANONICAL_SCENARIO = "nontrivial-build-research-first"
ALLOWED_MODES = {"template", "evidence"}
ALLOWED_STATUS = {"pending", "verified", "blocked"}
ALLOWED_CLIENTS = {"copilot-cli", "codex-cli", "claude-code", "gemini-cli", "cursor", "other"}
ALLOWED_VERDICTS = {"USE", "CONTRIBUTE", "FORK", "BUILD"}

SECRET_KEY_RE = re.compile(
    r"(?:^|[_-])(token|secret|password|passwd|authorization|cookie|credential|api[_-]?key)(?:$|[_-])",
    re.IGNORECASE,
)
SECRET_VALUE_PATTERNS = (
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]+=*", re.IGNORECASE),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
)


class EvidenceError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceError(message)


def non_empty_string(value: Any, path: str) -> str:
    require(isinstance(value, str) and value.strip(), f"{path} must be a non-empty string")
    return value.strip()


def validate_no_secrets(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            require(isinstance(key, str), f"{path}: object keys must be strings")
            require(not SECRET_KEY_RE.search(key), f"{path}.{key}: secret-like key is forbidden")
            validate_no_secrets(child, f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            validate_no_secrets(child, f"{path}[{index}]")
        return
    if isinstance(value, str):
        for pattern in SECRET_VALUE_PATTERNS:
            require(not pattern.search(value), f"{path}: secret-like value is forbidden")


def validate_iso_timestamp(value: Any, path: str) -> None:
    text = non_empty_string(value, path)
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceError(f"{path} must be ISO-8601") from exc


def validate_string_list(value: Any, path: str, *, allow_empty: bool) -> list[str]:
    require(isinstance(value, list), f"{path} must be an array")
    if not allow_empty:
        require(bool(value), f"{path} must not be empty")
    result: list[str] = []
    for index, item in enumerate(value):
        result.append(non_empty_string(item, f"{path}[{index}]"))
    return result


def validate_document(document: Any, source: str = "<memory>") -> None:
    require(isinstance(document, dict), f"{source}: root must be an object")
    validate_no_secrets(document)

    require(document.get("schemaVersion") == 1, f"{source}: schemaVersion must be 1")
    mode = document.get("mode")
    require(mode in ALLOWED_MODES, f"{source}: mode must be one of {sorted(ALLOWED_MODES)}")

    scenario_id = non_empty_string(document.get("scenarioId"), f"{source}: scenarioId")
    require(
        scenario_id == CANONICAL_SCENARIO,
        f"{source}: scenarioId must be canonical scenario {CANONICAL_SCENARIO!r}",
    )
    scenario_path = ROOT / "evals" / "github-build-or-reuse" / "tasks" / f"{scenario_id}.yaml"
    require(scenario_path.is_file(), f"{source}: scenario task does not exist: {scenario_path.relative_to(ROOT)}")

    plugin = document.get("plugin")
    require(isinstance(plugin, dict), f"{source}: plugin must be an object")
    require(plugin.get("name") == "github-build-or-reuse", f"{source}: plugin.name must be github-build-or-reuse")
    non_empty_string(plugin.get("version"), f"{source}: plugin.version")
    non_empty_string(plugin.get("source"), f"{source}: plugin.source")
    require(
        plugin.get("canonicalSkillPath") == "skills/github-build-or-reuse/SKILL.md",
        f"{source}: plugin.canonicalSkillPath must point to the canonical skill",
    )

    client = document.get("client")
    require(isinstance(client, dict), f"{source}: client must be an object")
    require(client.get("name") in ALLOWED_CLIENTS, f"{source}: client.name must be one of {sorted(ALLOWED_CLIENTS)}")
    non_empty_string(client.get("version"), f"{source}: client.version")

    environment = document.get("environment")
    require(isinstance(environment, dict), f"{source}: environment must be an object")
    non_empty_string(environment.get("platform"), f"{source}: environment.platform")
    require(environment.get("containsSensitiveData") is False, f"{source}: environment.containsSensitiveData must be false")

    validate_iso_timestamp(document.get("capturedAt"), f"{source}: capturedAt")

    execution = document.get("execution")
    require(isinstance(execution, dict), f"{source}: execution must be an object")
    status = execution.get("status")
    require(status in ALLOWED_STATUS, f"{source}: execution.status must be one of {sorted(ALLOWED_STATUS)}")

    if mode == "template":
        require(status == "pending", f"{source}: template execution.status must be pending")
        require(execution.get("skillActivated") in {None, False}, f"{source}: template must not claim skill activation")
        validate_string_list(execution.get("evidenceGatheringPath"), f"{source}: execution.evidenceGatheringPath", allow_empty=True)
        require(execution.get("verdict") is None, f"{source}: template verdict must be null")
        validate_string_list(execution.get("degradedOrUnknownChecks"), f"{source}: execution.degradedOrUnknownChecks", allow_empty=True)
        return

    require(status in {"verified", "blocked"}, f"{source}: evidence mode cannot remain pending")

    if status == "blocked":
        non_empty_string(execution.get("blockedReason"), f"{source}: execution.blockedReason")
        return

    require(execution.get("skillActivated") is True, f"{source}: verified evidence requires skillActivated=true")
    validate_string_list(execution.get("evidenceGatheringPath"), f"{source}: execution.evidenceGatheringPath", allow_empty=False)
    verdict = execution.get("verdict")
    require(verdict in ALLOWED_VERDICTS, f"{source}: execution.verdict must be one of {sorted(ALLOWED_VERDICTS)}")
    validate_string_list(execution.get("degradedOrUnknownChecks"), f"{source}: execution.degradedOrUnknownChecks", allow_empty=True)
    non_empty_string(execution.get("resultSummary"), f"{source}: execution.resultSummary")
    non_empty_string(execution.get("sanitizedOutput"), f"{source}: execution.sanitizedOutput")


def evidence_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(path for path in directory.glob("*.json") if path.is_file())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, help="Evidence JSON files; defaults to evidence/behavioral/*.json")
    args = parser.parse_args()

    paths = args.paths or evidence_files(DEFAULT_EVIDENCE_DIR)
    if not paths:
        print("OK: no behavioral runtime evidence files to validate")
        return 0

    failures = 0
    for path in paths:
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
            validate_document(document, str(path))
        except (OSError, json.JSONDecodeError, EvidenceError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            failures += 1
        else:
            print(f"OK: {path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
