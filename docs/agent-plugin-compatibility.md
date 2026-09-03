# Agent Plugin compatibility and distribution contract

`github-build-or-reuse` uses **one canonical Agent Skill** and exposes it through multiple distribution surfaces. Agent Plugins 1.0 is an additional portable package format; it does not replace the Agent Skills or skills.sh paths.

## Canonical runtime source

The only runtime skill source is:

```text
skills/github-build-or-reuse/SKILL.md
```

Both Agent Plugins v1 and skills.sh must continue discovering that exact directory. A root `SKILL.md` or a platform-specific copy would create competing sources of truth and is rejected by repository validation.

## Stability contract for skills.sh

The following identifiers are release invariants unless a deliberate migration is planned:

- repository: `ghspain/github-build-or-reuse`;
- skill name: `github-build-or-reuse`;
- canonical path: `skills/github-build-or-reuse/SKILL.md`;
- skills.sh registration: `skills.sh.json` includes `github-build-or-reuse`;
- Agent Plugins discovery: the same skill is an immediate child of `skills/`.

`scripts/validate-agent-plugin.py` compares the Agent Plugins-discovered skill set with the skills registered in `skills.sh.json`. CI also executes `npx skills@latest add . --list` and requires `github-build-or-reuse` to be discovered. A packaging change that moves or renames the canonical skill without updating both contracts therefore fails before merge.

External skills.sh search/index ranking is not controlled by this repository, so it is not used as a blocking CI dependency. The repository instead preserves every stable input used by skills.sh discovery and validates the local CLI discovery path on every pull request.

## Agent Plugins 1.0 package

The portable package is rooted at the repository root:

```text
plugin.json
skills/
  github-build-or-reuse/
    SKILL.md
```

Agent Plugins 1.0 discovers skills from the fixed `skills/` location. `plugin.json` therefore contains only portable manifest metadata and does not duplicate a `skills` path field.

The package currently does **not** include `mcp.json`. The skill can collect GitHub evidence through host-native GitHub access, an existing GitHub MCP integration, authenticated `gh`, the GitHub API, or web research. A bespoke wrapper MCP would add maintenance and security surface without a demonstrated unique capability.

## Compatibility evidence matrix

Compatibility claims are deliberately separated by evidence strength.

| Surface | Current evidence | Classification |
| --- | --- | --- |
| Agent Plugins 1.0 root package | fixed-layout + closed-field validation in CI | conformance/discovery verified |
| Agent Skills reference format | upstream `skills-ref validate` in CI | format verified |
| skills.sh / `npx skills` | `npx skills@latest add . --list` in CI | local install/discovery verified |
| GitHub CLI `gh skill` | `gh skill publish --dry-run` when runner CLI supports it | publish-path verified when available |
| Codex adapter | generated from canonical distribution config | manifest compatibility; runtime verification pending |
| Claude Code adapter | generated from canonical distribution config | manifest compatibility; runtime verification pending |
| Cursor adapter | generated from canonical distribution config | manifest compatibility; runtime verification pending |
| Gemini CLI adapter | generated from canonical distribution config | manifest compatibility; runtime verification pending |
| GitHub Agentic Workflows | no runtime evidence captured yet | pending |

Do not rewrite a **manifest compatibility** result as "runs everywhere". Runtime claims should include client/version/date and the command or evidence used to verify them.

## Host-specific adapters

`.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/`, `marketplace.json`, and `gemini-extension.json` are compatibility/distribution outputs generated from canonical state. They must not become independent runtime copies.

Regenerate and check them with:

```bash
python scripts/generate-distribution.py
python scripts/generate-distribution.py --check
```

## Security baseline

A distributable change must preserve these properties:

- no secrets or credentials in plugin metadata;
- portable `plugin.json` only uses Agent Plugins v1 fields;
- referenced skill content stays inside the repository package;
- external Actions remain full-SHA pinned with explicit permissions and timeouts;
- no MCP server or network endpoint is bundled without a concrete capability requirement and review;
- license/provenance information remains intact;
- runtime compatibility is stated at the evidence level actually verified.
