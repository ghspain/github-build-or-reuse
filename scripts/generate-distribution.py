#!/usr/bin/env python3
"""Generate standalone cross-agent manifests from canonical skill metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "distribution.config.json"
METADATA_PATH = ROOT / "metadata.yaml"
SKILL_PATH = ROOT / "skills" / "github-build-or-reuse" / "SKILL.md"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
GENERATED_PATHS = (
    Path("plugin.json"),
    Path("marketplace.json"),
    Path(".agents/plugins/marketplace.json"),
    Path(".codex-plugin/plugin.json"),
    Path(".claude-plugin/plugin.json"),
    Path(".claude-plugin/marketplace.json"),
    Path(".cursor-plugin/marketplace.json"),
    Path("gemini-extension.json"),
)


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


def load_yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        fail(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)}: expected a mapping")
    return data


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)}: missing frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail(f"{path.relative_to(ROOT)}: unclosed frontmatter")
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        fail(f"{path.relative_to(ROOT)}: invalid frontmatter: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)}: frontmatter must be a mapping")
    return data


def canonical_state() -> tuple[dict, str]:
    config = load_json(CONFIG_PATH)
    metadata = load_yaml(METADATA_PATH)
    skill = frontmatter(SKILL_PATH)
    if config.get("schemaVersion") != 1:
        fail("distribution.config.json: schemaVersion must be 1")
    name = config.get("name")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name):
        fail("distribution.config.json: invalid name")
    if metadata.get("name") != name or skill.get("name") != name:
        fail("distribution name, repository metadata name and runtime skill name must match")
    version = metadata.get("version")
    skill_version = (skill.get("metadata") or {}).get("version") if isinstance(skill.get("metadata"), dict) else None
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("metadata.yaml: version must be semantic X.Y.Z")
    if skill_version != version:
        fail(f"SKILL.md version {skill_version!r} must match metadata.yaml version {version!r}")
    author = config.get("author")
    if not isinstance(author, dict) or not author.get("name") or not author.get("url"):
        fail("distribution.config.json: author requires name and url")
    return config, version


def dump(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def render(config: dict, version: str) -> dict[Path, str]:
    name = config["name"]
    description = config["description"]
    author = config["author"]
    interface = {
        "displayName": config["displayName"],
        "shortDescription": config["shortDescription"],
        "longDescription": config["longDescription"],
        "developerName": author["name"],
        "category": config["category"],
        "capabilities": ["Read"],
        "websiteURL": config["homepage"],
        "defaultPrompt": config["defaultPrompt"],
    }
    portable = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": name,
        "version": version,
        "description": description,
        "author": author,
        "homepage": config["homepage"],
        "repository": config["repository"],
        "license": config["license"],
        "keywords": config["keywords"],
    }
    host_plugin = {
        "name": name,
        "version": version,
        "description": description,
        "author": author,
        "homepage": config["homepage"],
        "repository": config["repository"],
        "license": config["license"],
        "keywords": config["keywords"],
        "skills": "./skills/",
        "interface": interface,
    }
    marketplace = {
        "name": name,
        "owner": author,
        "metadata": {"description": description},
        "plugins": [{"name": name, "source": "./", "description": description, "version": version}],
    }
    market = config["marketplace"]
    agents_marketplace = {
        "name": market["name"],
        "interface": {"displayName": market["displayName"]},
        "plugins": [{
            "name": name,
            "source": {"source": "url", "url": market["sourceUrl"], "ref": market["ref"]},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": config["category"],
        }],
    }
    claude_marketplace = {
        "name": name,
        "description": description,
        "owner": author,
        "plugins": [{"name": name, "source": "./", "description": description, "version": version}],
    }
    cursor_marketplace = {
        "name": name,
        "owner": {"name": author["name"]},
        "metadata": {"description": description},
        "plugins": [{"name": name, "source": "./", "description": description}],
    }
    gemini = {"name": name, "version": version, "description": description}
    return {
        Path("plugin.json"): dump(portable),
        Path("marketplace.json"): dump(marketplace),
        Path(".agents/plugins/marketplace.json"): dump(agents_marketplace),
        Path(".codex-plugin/plugin.json"): dump(host_plugin),
        Path(".claude-plugin/plugin.json"): dump(host_plugin),
        Path(".claude-plugin/marketplace.json"): dump(claude_marketplace),
        Path(".cursor-plugin/marketplace.json"): dump(cursor_marketplace),
        Path("gemini-extension.json"): dump(gemini),
    }


def check(outputs: dict[Path, str]) -> int:
    drift: list[str] = []
    for relative, expected in outputs.items():
        target = ROOT / relative
        if not target.is_file():
            drift.append(f"{relative}: missing")
        elif target.read_text(encoding="utf-8") != expected:
            drift.append(f"{relative}: stale")
    if drift:
        for item in drift:
            print(f"DRIFT: {item}", file=sys.stderr)
        print("Run `python scripts/generate-distribution.py` and commit the outputs.", file=sys.stderr)
        return 1
    print(f"OK: {len(outputs)} standalone cross-agent manifests match canonical state")
    return 0


def write(outputs: dict[Path, str]) -> int:
    changed = 0
    for relative, content in outputs.items():
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_text(encoding="utf-8") == content:
            continue
        target.write_text(content, encoding="utf-8")
        print(f"WROTE: {relative}")
        changed += 1
    print(f"OK: {changed} manifest(s) updated")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    config, version = canonical_state()
    outputs = render(config, version)
    if set(outputs) != set(GENERATED_PATHS):
        fail("internal generated path mismatch")
    return check(outputs) if args.check else write(outputs)


if __name__ == "__main__":
    raise SystemExit(main())
