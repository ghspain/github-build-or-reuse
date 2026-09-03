#!/usr/bin/env python3
"""Enforce the repository GitHub Actions security baseline."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
WRITE_PERMISSION_RE = re.compile(r"(?:^|-)(?:write|admin)$")


def fail(errors: list[str]) -> None:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)


def load_workflow(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        fail([f"{path.relative_to(ROOT)}: invalid YAML: {exc}"])
    if not isinstance(data, dict):
        fail([f"{path.relative_to(ROOT)}: workflow must be a YAML mapping"])
    return data


def has_write_permission(permissions: dict) -> bool:
    return any(isinstance(value, str) and WRITE_PERMISSION_RE.search(value) for value in permissions.values())


def validate(path: Path) -> list[str]:
    data = load_workflow(path)
    rel = path.relative_to(ROOT)
    errors: list[str] = []
    triggers = data.get("on", data.get(True))
    if isinstance(triggers, dict) and "pull_request_target" in triggers:
        errors.append(f"{rel}: pull_request_target is forbidden")
    permissions = data.get("permissions")
    if not isinstance(permissions, dict) or not permissions:
        errors.append(f"{rel}: declare explicit top-level permissions")
        permissions = {}
    if path.name == "validate.yml" and has_write_permission(permissions):
        errors.append(f"{rel}: validation workflow must remain read-only")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        errors.append(f"{rel}: jobs mapping is missing or empty")
        return errors
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            errors.append(f"{rel}: job {job_name!r} must be a mapping")
            continue
        timeout = job.get("timeout-minutes")
        if not isinstance(timeout, int) or timeout <= 0:
            errors.append(f"{rel}: job {job_name!r} requires positive timeout-minutes")
        for index, step in enumerate(job.get("steps", []) or [], start=1):
            if not isinstance(step, dict):
                continue
            uses = step.get("uses")
            location = f"{rel}: job {job_name!r} step {index}"
            if isinstance(uses, str) and not uses.startswith("./"):
                if "@" not in uses or not SHA_RE.fullmatch(uses.rsplit("@", 1)[1]):
                    errors.append(f"{location}: external action must be pinned to a full commit SHA")
                action = uses.rsplit("@", 1)[0] if "@" in uses else uses
                if action == "actions/checkout":
                    with_block = step.get("with")
                    persist = with_block.get("persist-credentials") if isinstance(with_block, dict) else None
                    if persist is not False:
                        errors.append(f"{location}: checkout must set persist-credentials: false")
            run = step.get("run")
            if isinstance(run, str):
                for line in run.splitlines():
                    if line.strip().startswith("npm ci") and "--ignore-scripts" not in line:
                        errors.append(f"{location}: npm ci must use --ignore-scripts")
    return errors


def main() -> None:
    workflows = sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])
    errors: list[str] = []
    for path in workflows:
        errors.extend(validate(path))
    if errors:
        fail(errors)
    print(f"OK: {len(workflows)} workflow(s) satisfy the repository security baseline")


if __name__ == "__main__":
    main()
