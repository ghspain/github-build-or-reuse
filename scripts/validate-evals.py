#!/usr/bin/env python3
"""Validate the canonical Waza suite without model credentials."""

from __future__ import annotations

from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "evals" / "github-build-or-reuse"
SKILL_PATH = "skills/github-build-or-reuse/SKILL.md"


def load(path: Path) -> dict:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"missing or unsafe {path.relative_to(ROOT)}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)}: expected mapping")
    return data


def main() -> None:
    errors: list[str] = []
    try:
        spec = load(SUITE / "eval.yaml")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

    if spec.get("skill") != "github-build-or-reuse":
        errors.append("eval.yaml: skill must be github-build-or-reuse")
    if spec.get("schemaVersion") != "1.2":
        errors.append("eval.yaml: schemaVersion must be '1.2'")
    if spec.get("tasks") != ["tasks/*.yaml"]:
        errors.append("eval.yaml: tasks must be exactly ['tasks/*.yaml']")
    config = spec.get("config")
    if not isinstance(config, dict) or config.get("executor") != "copilot-sdk":
        errors.append("eval.yaml: config.executor must be copilot-sdk")

    tasks = sorted((SUITE / "tasks").glob("*.yaml"))
    if len(tasks) < 5:
        errors.append(f"expected at least five intrinsic behavior tasks, found {len(tasks)}")
    ids: set[str] = set()
    positives = negatives = behavioral = 0
    for path in tasks:
        try:
            task = load(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id:
            errors.append(f"{path.relative_to(ROOT)}: id required")
            continue
        if task_id in ids:
            errors.append(f"duplicate task id {task_id!r}")
        ids.add(task_id)
        expected = task.get("expected")
        if not isinstance(expected, dict) or not isinstance(expected.get("should_trigger"), bool):
            errors.append(f"{path.relative_to(ROOT)}: boolean expected.should_trigger required")
            continue
        should_trigger = expected["should_trigger"]
        positives += int(should_trigger)
        negatives += int(not should_trigger)
        graders = expected.get("graders")
        if not isinstance(graders, list) or not graders:
            errors.append(f"{path.relative_to(ROOT)}: graders required")
            continue
        trigger = [g for g in graders if isinstance(g, dict) and g.get("type") == "trigger"]
        if len(trigger) != 1:
            errors.append(f"{path.relative_to(ROOT)}: exactly one trigger grader required")
            continue
        trigger_config = trigger[0].get("config")
        expected_mode = "positive" if should_trigger else "negative"
        if not isinstance(trigger_config, dict) or trigger_config.get("skill_path") != SKILL_PATH or trigger_config.get("mode") != expected_mode:
            errors.append(f"{path.relative_to(ROOT)}: trigger grader must target {SKILL_PATH} in {expected_mode} mode")
        non_trigger = [g for g in graders if isinstance(g, dict) and g.get("type") != "trigger"]
        behavioral += len(non_trigger)
        if should_trigger and not non_trigger:
            errors.append(f"{path.relative_to(ROOT)}: positive task requires behavioral grader")

    if positives == 0 or negatives == 0:
        errors.append("suite requires both positive and negative trigger cases")
    if behavioral == 0:
        errors.append("suite requires behavioral grading")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: canonical Waza suite validates with {len(tasks)} tasks")


if __name__ == "__main__":
    main()
