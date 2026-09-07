#!/usr/bin/env python3
"""Validate the repository's importable immutable release-tag ruleset recipe."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RULESET = ROOT / ".github" / "rulesets" / "immutable-release-tags.json"
EXPECTED_NAME = "Immutable release tags v*"
EXPECTED_RULES = {"deletion", "update", "non_fast_forward"}
EXPECTED_PATTERN = "refs/tags/v*"


def fail(message: str) -> "NoReturn":
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    try:
        data = json.loads(RULESET.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{RULESET.relative_to(ROOT)}: invalid JSON: {exc}")

    if not isinstance(data, dict):
        fail("ruleset root must be a JSON object")
    if data.get("name") != EXPECTED_NAME:
        fail(f"ruleset name must remain {EXPECTED_NAME!r}")
    if data.get("target") != "tag":
        fail("ruleset target must be 'tag'")
    if data.get("enforcement") != "active":
        fail("ruleset enforcement must be 'active'")

    unexpected_top_level = set(data) - {"name", "target", "enforcement", "conditions", "rules", "bypass_actors"}
    if unexpected_top_level:
        fail(f"unexpected top-level fields: {sorted(unexpected_top_level)}")

    bypass = data.get("bypass_actors", [])
    if bypass not in (None, []):
        fail("release tag ruleset must not define bypass actors by default")

    conditions = data.get("conditions")
    if not isinstance(conditions, dict) or set(conditions) != {"ref_name"}:
        fail("repository-level ruleset conditions must contain only ref_name")
    ref_name = conditions["ref_name"]
    if not isinstance(ref_name, dict):
        fail("conditions.ref_name must be an object")
    if ref_name.get("include") != [EXPECTED_PATTERN]:
        fail(f"ruleset must target exactly {EXPECTED_PATTERN!r}")
    if ref_name.get("exclude") != []:
        fail("release tag ruleset must not exclude matching v* tags")

    rules = data.get("rules")
    if not isinstance(rules, list) or not rules:
        fail("rules must be a non-empty array")
    observed: list[str] = []
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict) or set(rule) != {"type"}:
            fail(f"rules[{index}] must contain only a type field")
        rule_type = rule.get("type")
        if not isinstance(rule_type, str):
            fail(f"rules[{index}].type must be a string")
        observed.append(rule_type)

    if set(observed) != EXPECTED_RULES or len(observed) != len(EXPECTED_RULES):
        fail(
            "release tags must be protected by exactly deletion, update, and "
            f"non_fast_forward; observed {observed}"
        )

    print(
        "OK: immutable release tag ruleset targets refs/tags/v* and blocks "
        "update, deletion, and non-fast-forward changes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
