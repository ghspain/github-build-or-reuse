#!/usr/bin/env python3
"""Dependency-free structural validation for github-build-or-reuse."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "metadata.yaml",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "references/decision-framework.md",
    "references/github-evidence.md",
    "references/licensing.md",
    "examples/presentation-generator.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")

    parts = skill.split("---\n", 2)
    if len(parts) < 3:
        fail("SKILL.md frontmatter is not closed")
    frontmatter = parts[1]

    expected = {
        "name": "github-build-or-reuse",
        "license": "MIT",
    }
    for key, value in expected.items():
        if not re.search(rf"^{re.escape(key)}:\s*{re.escape(value)}\s*$", frontmatter, re.MULTILINE):
            fail(f"SKILL.md frontmatter must contain {key}: {value}")

    description_match = re.search(r'^description:\s*"([^"]+)"\s*$', frontmatter, re.MULTILINE)
    if not description_match:
        fail("description must be a quoted single physical line")
    description = description_match.group(1)
    if not 10 <= len(description) <= 250:
        fail("description must contain 10-250 characters")

    for token in ("USE", "CONTRIBUTE", "FORK", "BUILD"):
        if token not in skill:
            fail(f"SKILL.md must preserve decision token {token}")

    metadata = (ROOT / "metadata.yaml").read_text(encoding="utf-8")
    for required in (
        "name: github-build-or-reuse",
        "origin:",
        "category: github",
        "status: active",
    ):
        if required not in metadata:
            fail(f"metadata.yaml missing {required}")

    local_docs = [ROOT / "SKILL.md", ROOT / "README.md", *sorted((ROOT / "references").glob("*.md"))]
    for path in local_docs:
        text = path.read_text(encoding="utf-8")
        if "../../" in text or "../skills/" in text:
            fail(f"{path.relative_to(ROOT)} contains a parent-repository dependency")

    print("OK: github-build-or-reuse structure is valid")


if __name__ == "__main__":
    main()
