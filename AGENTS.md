# Agent instructions

This repository publishes one portable Agent Skill and platform packaging around it.

## Source of truth

- Canonical runtime skill: `skills/github-build-or-reuse/`
- Portable Agent Plugins v1 manifest: `plugin.json`
- skills.sh grouping metadata: `skills.sh.json`
- Generated host adapters: `.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/`, `marketplace.json`, `gemini-extension.json`
- Project docs: `docs/`
- README demo evidence: `assets/demo.json`
- Demo generator: `scripts/generate_demo.py`
- Distribution generator: `scripts/generate-distribution.py`
- Repository validation: `scripts/validate.py`
- Agent Plugin / skills.sh contract validation: `scripts/validate-agent-plugin.py`

Do not recreate a second root `SKILL.md` or duplicate the canonical skill into platform-specific directories.

## Distribution invariants

- Agent Plugins adoption complements Agent Skills and skills.sh; it does not replace them.
- Preserve repository `ghspain/github-build-or-reuse`, skill name `github-build-or-reuse`, and path `skills/github-build-or-reuse/SKILL.md` unless a deliberate migration is explicitly planned.
- `skills.sh.json` and Agent Plugins fixed discovery from `skills/*/SKILL.md` must expose the same canonical skill set.
- Keep `plugin.json` portable: Agent Plugins v1 fields only. Host-specific metadata belongs in generated adapters/extensions, not invented top-level fields.
- Do not claim runtime compatibility merely because a host manifest can be generated. Classify evidence as manifest-only, install/discovery verified, or runtime verified.

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
python scripts/validate-agent-plugin.py
python scripts/generate-distribution.py --check
python scripts/generate_demo.py --check
```

CI additionally validates the canonical directory against the Agent Skills reference validator, verifies `npx skills` discovery, and checks that generated distribution/demo assets match their canonical sources.
