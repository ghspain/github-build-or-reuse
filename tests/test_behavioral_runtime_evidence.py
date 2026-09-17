from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate-behavioral-runtime-evidence.py"
SPEC = importlib.util.spec_from_file_location("behavioral_evidence", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def verified_document() -> dict:
    return {
        "schemaVersion": 1,
        "mode": "evidence",
        "scenarioId": "nontrivial-build-research-first",
        "plugin": {
            "name": "github-build-or-reuse",
            "version": "1.2.3",
            "source": "github-build-or-reuse@github-build-or-reuse",
            "canonicalSkillPath": "skills/github-build-or-reuse/SKILL.md",
        },
        "client": {"name": "copilot-cli", "version": "1.0.85"},
        "environment": {"platform": "linux-x64", "containsSensitiveData": False},
        "capturedAt": "2026-09-17T20:00:00Z",
        "execution": {
            "status": "verified",
            "skillActivated": True,
            "evidenceGatheringPath": ["GitHub repository search", "repository inspection"],
            "verdict": "USE",
            "degradedOrUnknownChecks": ["live adoption signal unavailable"],
            "resultSummary": "Existing project covers the requested capability and was selected after due diligence.",
            "sanitizedOutput": "Researched alternatives before implementation and converged on USE.",
            "blockedReason": "",
        },
    }


class BehavioralEvidenceTests(unittest.TestCase):
    def test_template_is_valid(self) -> None:
        document = json.loads((ROOT / "evidence" / "behavioral" / "TEMPLATE.json").read_text())
        MODULE.validate_document(document, "template")

    def test_verified_evidence_is_valid(self) -> None:
        MODULE.validate_document(verified_document(), "verified")

    def test_verified_requires_activation(self) -> None:
        document = verified_document()
        document["execution"]["skillActivated"] = False
        with self.assertRaisesRegex(MODULE.EvidenceError, "skillActivated=true"):
            MODULE.validate_document(document, "no-activation")

    def test_verified_requires_evidence_path(self) -> None:
        document = verified_document()
        document["execution"]["evidenceGatheringPath"] = []
        with self.assertRaisesRegex(MODULE.EvidenceError, "must not be empty"):
            MODULE.validate_document(document, "no-path")

    def test_rejects_noncanonical_scenario(self) -> None:
        document = verified_document()
        document["scenarioId"] = "trivial-snippet-boundary"
        with self.assertRaisesRegex(MODULE.EvidenceError, "canonical scenario"):
            MODULE.validate_document(document, "wrong-scenario")

    def test_rejects_secret_like_key(self) -> None:
        document = verified_document()
        document["execution"]["api_key"] = "redacted"
        with self.assertRaisesRegex(MODULE.EvidenceError, "secret-like key"):
            MODULE.validate_document(document, "secret-key")

    def test_rejects_secret_like_value(self) -> None:
        document = verified_document()
        document["execution"]["sanitizedOutput"] = "Bearer abcdefghijklmnopqrstuvwxyz012345"
        with self.assertRaisesRegex(MODULE.EvidenceError, "secret-like value"):
            MODULE.validate_document(document, "secret-value")

    def test_evidence_mode_cannot_remain_pending(self) -> None:
        document = verified_document()
        document["execution"]["status"] = "pending"
        with self.assertRaisesRegex(MODULE.EvidenceError, "cannot remain pending"):
            MODULE.validate_document(document, "pending-evidence")


if __name__ == "__main__":
    unittest.main()
