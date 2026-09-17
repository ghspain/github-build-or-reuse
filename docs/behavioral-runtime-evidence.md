# Cross-client behavioral runtime evidence

This procedure supports issue #35. It does **not** replace the intrinsic eval suite under `evals/github-build-or-reuse/`; it records comparable evidence from real client sessions after the skill has been installed through the client's supported Agent Plugin path.

## Canonical scenario

Use the existing eval task:

```text
evals/github-build-or-reuse/tasks/nontrivial-build-research-first.yaml
```

Scenario id:

```text
nontrivial-build-research-first
```

Canonical prompt:

> Build me a self-hosted AI presentation generator that exports editable PPTX files. Start implementing it now.

The expected behavior already defined by the eval is that `github-build-or-reuse` activates, performs or explicitly attempts GitHub/open-source due diligence **before substantial implementation**, and converges on one of:

```text
USE | CONTRIBUTE | FORK | BUILD
```

Do not create a second prompt for Copilot and Codex. The point of #35 is parity on the same representative scenario.

## Capture procedure

1. Install the released plugin through the client's normal native Agent Plugin path.
2. Record the exact client version and installed plugin version/source.
3. Start a trusted model session with whatever normal GitHub/web research access that client supports.
4. Submit the canonical prompt unchanged.
5. Record whether the skill activated and which evidence-gathering path was actually used.
6. Record the final `USE`, `CONTRIBUTE`, `FORK`, or `BUILD` verdict.
7. Record degraded or unknown checks explicitly instead of silently treating them as verified.
8. Save only a concise **sanitized** result/output. Do not commit full session state, auth config, tokens, cookies, PATs, API keys, OAuth material, or credential-bearing logs.

Copy the template:

```bash
cp evidence/behavioral/TEMPLATE.json evidence/behavioral/<client>-<date>.json
```

Change:

```json
"mode": "evidence"
```

and set `execution.status` to either:

- `verified` — only when all required behavioral evidence exists; or
- `blocked` — when the trusted client/session could not complete the scenario, with `blockedReason` explaining why.

A real evidence file must not remain `pending`.

## Validation

Run:

```bash
python scripts/validate-behavioral-runtime-evidence.py
python -m unittest tests.test_behavioral_runtime_evidence
```

For `verified` evidence, the validator requires:

- canonical scenario id;
- canonical skill identity/path;
- exact client and plugin versions/source;
- `skillActivated: true`;
- at least one evidence-gathering path;
- a valid USE / CONTRIBUTE / FORK / BUILD verdict;
- explicit degraded/unknown checks (empty is allowed when none exist);
- non-empty result summary and sanitized output;
- `containsSensitiveData: false`;
- no common secret-bearing keys or token/PAT/JWT/Bearer patterns.

## Parity decision

Do not treat one passing client as cross-client parity. Issue #35 requires the same scenario to be captured for at least:

- GitHub Copilot / Copilot CLI;
- OpenAI Codex.

Install/discovery or lifecycle/update evidence does not satisfy this behavioral gate. Adapter retirement, if any, must still be a separate evidence-backed PR after the two runtime records are reviewed.
