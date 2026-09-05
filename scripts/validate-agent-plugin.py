#!/usr/bin/env python3
"""Validate the portable Agent Plugin without regressing skills.sh discovery."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILL = "github-build-or-reuse"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
SKILLS_SH_SCHEMA = "https://skills.sh/schemas/skills.sh.schema.json"
PORTABLE_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def fail(message: str) -> "NoReturn":
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)}: expected an object")
    return data


def plugin_skills() -> set[str]:
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        fail("Agent Plugins fixed skills/ directory is missing")
    discovered = {
        child.name
        for child in skills_dir.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    if not discovered:
        fail("Agent Plugin discovers no skills from skills/*/SKILL.md")
    return discovered


def skills_sh_skills(config: dict) -> list[str]:
    if config.get("$schema") != SKILLS_SH_SCHEMA:
        fail("skills.sh.json must preserve the canonical skills.sh schema")
    groupings = config.get("groupings")
    if not isinstance(groupings, list):
        fail("skills.sh.json groupings must be a list")
    skills: list[str] = []
    for grouping in groupings:
        if not isinstance(grouping, dict) or not isinstance(grouping.get("skills"), list):
            fail("each skills.sh grouping must contain a skills list")
        for skill in grouping["skills"]:
            if not isinstance(skill, str):
                fail("skills.sh skill names must be strings")
            skills.append(skill)
    if len(skills) != len(set(skills)):
        fail("skills.sh.json contains duplicate skill registrations")
    return skills


def validate_manifest(plugin: dict) -> str:
    unknown = sorted(set(plugin) - PORTABLE_FIELDS)
    if unknown:
        fail("plugin.json has non-portable top-level fields: " + ", ".join(unknown))
    if plugin.get("$schema") != PLUGIN_SCHEMA:
        fail("plugin.json must target Agent Plugins 1.0.0")
    name = plugin.get("name")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name):
        fail("plugin.json name is invalid")
    version = plugin.get("version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        fail("plugin.json version must be semantic X.Y.Z")
    for field in ("description", "homepage", "repository", "license"):
        if not isinstance(plugin.get(field), str) or not plugin[field].strip():
            fail(f"plugin.json {field} must be a non-empty string")
    author = plugin.get("author")
    if not isinstance(author, dict) or not isinstance(author.get("name"), str) or not author["name"].strip():
        fail("plugin.json author.name is required")
    keywords = plugin.get("keywords")
    if not isinstance(keywords, list) or not keywords or not all(isinstance(item, str) and item for item in keywords):
        fail("plugin.json keywords must be a non-empty string list")
    if "skills" in plugin:
        fail("Agent Plugins v1 discovers skills from fixed skills/; plugin.json must not declare a skills field")
    extensions = plugin.get("extensions")
    if extensions is not None and not isinstance(extensions, dict):
        fail("plugin.json extensions must be an object when present")
    return version


def main() -> None:
    if (ROOT / "SKILL.md").exists():
        fail("root SKILL.md would create a second source of truth")

    plugin = load_json(ROOT / "plugin.json")
    version = validate_manifest(plugin)
    if plugin.get("name") != EXPECTED_SKILL:
        fail(f"portable plugin name must remain {EXPECTED_SKILL}")

    discovered = plugin_skills()
    if discovered != {EXPECTED_SKILL}:
        fail(f"portable plugin skill set changed unexpectedly: {sorted(discovered)}")

    skills_sh = load_json(ROOT / "skills.sh.json")
    indexed = set(skills_sh_skills(skills_sh))
    if indexed != discovered:
        fail(
            "skills.sh and Agent Plugins must expose the same canonical skill set; "
            f"skills.sh={sorted(indexed)} plugin={sorted(discovered)}"
        )

    metadata = (ROOT / "metadata.yaml").read_text(encoding="utf-8")
    metadata_match = re.search(r'^version:\s*["\']?(\d+\.\d+\.\d+)["\']?\s*$', metadata, re.MULTILINE)
    if not metadata_match or metadata_match.group(1) != version:
        fail("plugin.json version must match metadata.yaml")

    skill_text = (ROOT / "skills" / EXPECTED_SKILL / "SKILL.md").read_text(encoding="utf-8")
    skill_match = re.search(r'^\s{2}version:\s*["\'](\d+\.\d+\.\d+)["\']\s*$', skill_text, re.MULTILINE)
    if not skill_match or skill_match.group(1) != version:
        fail("plugin.json version must match canonical SKILL.md metadata.version")

    for adapter in (ROOT / ".codex-plugin/plugin.json", ROOT / ".claude-plugin/plugin.json"):
        data = load_json(adapter)
        if data.get("skills") != "./skills/":
            fail(f"{adapter.relative_to(ROOT)} must continue referencing ./skills/")
        if data.get("name") != EXPECTED_SKILL or data.get("version") != version:
            fail(f"{adapter.relative_to(ROOT)} identity/version drifted from portable package")

    print(
        "OK: Agent Plugins v1 and skills.sh expose the same canonical "
        f"{EXPECTED_SKILL} skill at version {version}"
    )


if __name__ == "__main__":
    main()
