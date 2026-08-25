# Agent instructions

This repository contains a runtime skill, not a generic tutorial.

## Principles

- Keep `SKILL.md` concise and imperative. Put explanation, examples, command recipes, and edge cases in `references/` or `examples/`.
- Preserve the primary decision vocabulary: `USE`, `CONTRIBUTE`, `FORK`, `BUILD`.
- Keep the skill tool-agnostic. Prefer structured GitHub evidence, but do not require one vendor-specific agent runtime.
- Verify current GitHub CLI/API capabilities before adding or changing command examples.
- Do not use star count as a quality score. Historical star trends may be context, never causal proof by themselves.
- Treat licensing statements conservatively and separate engineering triage from legal advice.
- Do not add private repository names, credentials, tokens, personal paths, or user-specific data.
- Any new scoring factor must explain what evidence supports it and how missing evidence is handled.

## Validation

Run:

```bash
python scripts/validate.py
```

When this directory is extracted into its own repository, `.github/workflows/validate.yml` runs the same validation in CI.
