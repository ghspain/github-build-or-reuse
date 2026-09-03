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

`.github/workflows/eval-behavioral.yml` runs manually or weekly from trusted repository state. It uses `COPILOT_SDK_TOKEN` when configured and otherwise exits safely with a notice instead of turning a missing credential into repository failure.

Successful/failed execution evidence is retained as JSON, JUnit and transcripts for 14 days. A pass describes the measured Waza/Copilot-SDK executor; it does not claim identical behavior in every host.

## Upstream vs catalog responsibility

This repository tests product behavior. A downstream catalog such as `svg153/skills` should test only integration/routing concerns specific to the multi-skill environment, not maintain a second copy of these five intrinsic cases.
