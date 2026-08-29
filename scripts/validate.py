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
    ROOT / ".github/labels.json",
    ROOT / ".github/workflows/release.yml",
    ROOT / ".github/workflows/repository-config.yml",
    ROOT / ".github/workflows/validate.yml",
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "NOTICE.md",
    ROOT / "metadata.yaml",
    ROOT / "skills.sh.json",
    ROOT / "AGENTS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "GOVERNANCE.md",
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


def require_match(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        fail(f"could not resolve {label}")
    return match.group(1)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    if (ROOT / "SKILL.md").exists():
        fail("root SKILL.md must not duplicate the canonical skill")

    metadata_text = (ROOT / "metadata.yaml").read_text(encoding="utf-8")
    version = require_match(
        r'^version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?\s*$',
        metadata_text,
        "semantic version from metadata.yaml",
    )

    for required in (
        "origin: https://github.com/ghspain/github-build-or-reuse",
        "origin_path: skills/github-build-or-reuse",
    ):
        if required not in metadata_text:
            fail(f"metadata.yaml missing {required}")

    release_notes = ROOT / "docs" / "releases" / f"v{version}.md"
    if not release_notes.is_file():
        fail(f"missing release notes for v{version}: {release_notes.relative_to(ROOT)}")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(rf"^## \[{re.escape(version)}\](?:\s|$)", changelog, re.MULTILINE):
        fail(f"CHANGELOG.md has no section for {version}")

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

    skill_version = require_match(
        r'^\s{2}version:\s*["\']([^"\']+)["\']\s*$',
        frontmatter,
        "skill version from SKILL.md metadata",
    )
    if skill_version != version:
        fail(f"SKILL.md version {skill_version} does not match repository version {version}")

    for token in ("USE", "CONTRIBUTE", "FORK", "BUILD"):
        if token not in skill_text:
            fail(f"SKILL.md must preserve decision token {token}")

    plugin = read_json(ROOT / ".codex-plugin/plugin.json")
    if plugin.get("name") != "github-build-or-reuse":
        fail("plugin name must be github-build-or-reuse")
    if plugin.get("skills") != "./skills/":
        fail("plugin must point skills to ./skills/")
    if plugin.get("version") != version:
        fail(f"plugin version {plugin.get('version')!r} does not match repository version {version}")

    marketplace = read_json(ROOT / ".agents/plugins/marketplace.json")
    entries = marketplace.get("plugins", [])
    if not any(item.get("name") == "github-build-or-reuse" for item in entries):
        fail("marketplace must expose github-build-or-reuse")

    skills_sh = read_json(ROOT / "skills.sh.json")
    groupings = skills_sh.get("groupings", [])
    grouped_skills = {
        skill
        for group in groupings
        for skill in group.get("skills", [])
    }
    if "github-build-or-reuse" not in grouped_skills:
        fail("skills.sh.json must expose github-build-or-reuse")

    labels = read_json(ROOT / ".github/labels.json")
    label_names = {item.get("name") for item in labels}
    for required_label in ("bug", "enhancement", "decision-quality", "triggering", "packaging", "security"):
        if required_label not in label_names:
            fail(f"labels.json missing required label {required_label}")

    evals = read_json(SKILL / "evals/evals.json")
    if evals.get("skill_name") != "github-build-or-reuse" or len(evals.get("evals", [])) < 3:
        fail("evals.json must contain at least three evals for the canonical skill")
    queries = read_json(SKILL / "evals/eval_queries.json")
    if not any(item.get("should_trigger") is True for item in queries):
        fail("trigger evals need positive examples")
    if not any(item.get("should_trigger") is False for item in queries):
        fail("trigger evals need negative examples")

    print(f"OK: github-build-or-reuse v{version} repository structure is valid")


if __name__ == "__main__":
    main()
