# Behavioral evaluations

The canonical repository owns the **intrinsic behavior** of `github-build-or-reuse`. Waza suites therefore live at top-level `evals/github-build-or-reuse/`, outside the portable runtime payload.

The suite protects five core behaviors:

- research before substantial implementation;
- evidence-based comparison with one `USE`, `CONTRIBUTE`, `FORK`, or `BUILD` verdict;
- explicit discovery bypass is honored and disclosed;
- trivial snippets do not force repository discovery;
- unavailable search/tooling is disclosed as an evidence gap rather than silently fabricated.

## Pull requests

PR validation is deterministic and does not receive a model credential:

```bash
python -m pip install 'PyYAML>=6,<7'
python scripts/validate-evals.py
bash scripts/install-waza-ci.sh /tmp/waza
/tmp/waza spec verify \
  --skill skills/github-build-or-reuse \
  --eval evals/github-build-or-reuse/eval.yaml
```

Waza is pinned to v0.38.6 and the Linux CI asset is checksum-verified.

## Trusted model-backed runs

`.github/workflows/eval-behavioral.yml` runs manually or weekly from trusted repository state. Successful/failed execution evidence is retained as JSON, JUnit, transcripts and the Waza log for 14 days. A pass describes the measured Waza/Copilot-SDK executor; it does not claim identical behavior in every host.

### Credentials

The workflow picks the first available option:

1. **`COPILOT_GITHUB_TOKEN` secret (user token).** A fine-grained personal access token with the account permission "Copilot Requests". Requests consume that user's premium-request quota. Set it with `gh secret set COPILOT_GITHUB_TOKEN -R ghspain/github-build-or-reuse`.
2. **Built-in `GITHUB_TOKEN` with `copilot-requests: write` (organization Copilot).** Only works when the owning organization has Copilot enabled with the Copilot CLI policy turned on and billing configured; requests are billed to the organization. No secret is needed.

If the organization has not enabled the CLI policy, Waza fails every task with `[ERROR] session error: Authorization error, you may need to run /login`. The workflow then writes an explicit failed summary pointing here. A run with no usable credential never reports a green model-backed result.

### Cost policy

- The weekly schedule is a change detector, not a fixed spend. The suite runs only when `skills/**`, `evals/**`, `scripts/install-waza-ci.sh` or the workflow itself changed since the last successful model-backed run; otherwise the run is skipped with a summary and zero premium requests.
- The last successful run is recorded as an `eval-baseline-<sha>` artifact (90 days). With no baseline the suite runs.
- `workflow_dispatch` accepts `force: true` to run regardless of changes.
- Every run's step summary reports the estimated premium requests (tasks x trials) and who is billed.

## Upstream vs catalog responsibility

This repository tests product behavior. A downstream catalog such as `svg153/skills` should test only integration/routing concerns specific to the multi-skill environment, not maintain a second copy of these five intrinsic cases.
