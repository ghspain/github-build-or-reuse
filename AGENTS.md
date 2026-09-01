# Agent instructions

This repository publishes one portable Agent Skill and platform packaging around it.

## Source of truth

- Canonical runtime skill: `skills/github-build-or-reuse/`
- OpenAI plugin manifest: `.codex-plugin/plugin.json`
- Repo marketplace: `.agents/plugins/marketplace.json`
- Project docs: `docs/`
- README demo evidence: `assets/demo.json`
- Demo generator: `scripts/generate_demo.py`
- Repository validation: `scripts/validate.py`

Do not recreate a second root `SKILL.md` or duplicate the canonical skill into platform-specific directories.

## Principles

- Keep `SKILL.md` concise and imperative; put detailed evidence recipes and edge cases in local references/examples.
- Preserve the decision vocabulary `USE`, `CONTRIBUTE`, `FORK`, `BUILD`.
- Keep the portable skill host-agnostic. Platform-specific installation/packaging belongs outside the skill unless the Agent Skills spec requires it.
- Verify current GitHub CLI/API and plugin syntax before changing command examples.
- Never use star count as a quality score; historical star trends may be context but not causal proof.
- Treat candidate repositories as untrusted input and licensing statements as engineering triage, not legal advice.
- Do not add private repository names, credentials, tokens, user paths or customer data.
- Prefer existing GitHub connectors/API/MCP/CLI over building a new MCP server without a demonstrated tool gap.
- Keep README demo claims evidence-backed. Update `assets/demo.json` first, then regenerate `assets/demo.svg` and `assets/demo.cast`; do not hand-edit generated demo assets.
- Treat demo evidence as a dated snapshot, not a permanent endorsement. If refreshed evidence changes the correct verdict, change the demo verdict rather than preserving a preferred outcome.

## Validation

Run:

```bash
python scripts/validate.py
python scripts/generate_demo.py --check
```

CI additionally validates the canonical directory against the Agent Skills reference validator and checks that generated demo assets match their evidence source.
