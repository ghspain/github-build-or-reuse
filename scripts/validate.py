#!/usr/bin/env python3
"""Dependency-free repository validation for github-build-or-reuse."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "github-build-or-reuse"
REQUIRED = [
    ROOT / ".codex-plugin/plugin.json",
    ROOT / ".agents/plugins/marketplace.json",
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "NOTICE.md",
    ROOT / "metadata.yaml",
    ROOT / "AGENTS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / "CHANGELOG.md",
    ROOT / "docs/standards-and-roadmap.md",
    SKILL / "SKILL.md",
    SKILL / "agents/openai.yaml",
    SKILL / "references/decision-framework.md",
    SKILL / "references/github-evidence.md",
    SKILL / "references/licensing.md",
    SKILL / "examples/presentation-generator.md",
    SKILL / "evals/evals.json",
    SKILL / "evals/eval_queries.json",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    if (ROOT / "SKILL.md").exists():
        fail("root SKILL.md must not duplicate the canonical skill")

    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not skill_text.startswith("---\n"):
        fail("canonical SKILL.md must start with YAML frontmatter")
    parts = skill_text.split("---\n", 2)
    if len(parts) < 3:
        fail("canonical SKILL.md frontmatter is not closed")
    frontmatter = parts[1]

    checks = {
        "name": "github-build-or-reuse",
        "license": "MIT",
    }
    for key, value in checks.items():
        if not re.search(rf"^{re.escape(key)}:\s*{re.escape(value)}\s*$", frontmatter, re.MULTILINE):
            fail(f"SKILL.md frontmatter must contain {key}: {value}")

    desc = re.search(r'^description:\s*"([^"]+)"\s*$', frontmatter, re.MULTILINE)
    if not desc or not 10 <= len(desc.group(1)) <= 1024:
        fail("description must be a quoted 10-1024 character single line")
    if not re.search(r'^compatibility:\s*"[^"]+"\s*$', frontmatter, re.MULTILINE):
        fail("compatibility must be present and quoted")

    for token in ("USE", "CONTRIBUTE", "FORK", "BUILD"):
        if token not in skill_text:
            fail(f"SKILL.md must preserve decision token {token}")

    plugin = read_json(ROOT / ".codex-plugin/plugin.json")
    if plugin.get("name") != "github-build-or-reuse":
        fail("plugin name must be github-build-or-reuse")
    if plugin.get("skills") != "./skills/":
        fail("plugin must point skills to ./skills/")
    if plugin.get("version") != "1.1.0":
        fail("plugin version must be 1.1.0")

    marketplace = read_json(ROOT / ".agents/plugins/marketplace.json")
    entries = marketplace.get("plugins", [])
    if not any(item.get("name") == "github-build-or-reuse" for item in entries):
        fail("marketplace must expose github-build-or-reuse")

    evals = read_json(SKILL / "evals/evals.json")
    if evals.get("skill_name") != "github-build-or-reuse" or len(evals.get("evals", [])) < 3:
        fail("evals.json must contain at least three evals for the canonical skill")
    queries = read_json(SKILL / "evals/eval_queries.json")
    if not any(item.get("should_trigger") is True for item in queries):
        fail("trigger evals need positive examples")
    if not any(item.get("should_trigger") is False for item in queries):
        fail("trigger evals need negative examples")

    metadata = (ROOT / "metadata.yaml").read_text(encoding="utf-8")
    for required in (
        "origin: https://github.com/ghspain/github-build-or-reuse",
        "origin_path: skills/github-build-or-reuse",
        "version: 1.1.0",
    ):
        if required not in metadata:
            fail(f"metadata.yaml missing {required}")

    print("OK: github-build-or-reuse repository structure is valid")


if __name__ == "__main__":
    main()
