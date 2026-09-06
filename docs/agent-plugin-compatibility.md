# Agent Plugin compatibility and distribution contract

`github-build-or-reuse` uses **one canonical Agent Skill** and exposes it through multiple distribution surfaces. Agent Plugins 1.0 is the preferred future package boundary; it does not create a second runtime implementation.

## Canonical runtime source

The only runtime skill source is:

```text
skills/github-build-or-reuse/SKILL.md
```

Both Agent Plugins v1 and skills.sh must continue discovering that exact directory during the current compatibility phase. A root `SKILL.md` or a platform-specific copy would create competing sources of truth and is rejected by repository validation.

An Agent Plugin may become the primary installable capability without replacing this file: Agent Skills are a standard component type inside Agent Plugins.

## Stability contract for skills.sh

The following identifiers are release invariants unless a deliberate migration is planned:

- repository: `ghspain/github-build-or-reuse`;
- skill name: `github-build-or-reuse`;
- canonical path: `skills/github-build-or-reuse/SKILL.md`;
- skills.sh registration: `skills.sh.json` includes `github-build-or-reuse`;
- Agent Plugins discovery: the same skill is an immediate child of `skills/`.

`scripts/validate-agent-plugin.py` compares the Agent Plugins-discovered skill set with the skills registered in `skills.sh.json`. CI also executes `npx skills@latest add . --list` and requires `github-build-or-reuse` to be discovered. A packaging change that moves or renames the canonical skill without updating both contracts therefore fails before merge.

External skills.sh search/index ranking is not controlled by this repository, so it is not used as a blocking CI dependency. The repository instead preserves every stable input used by skills.sh discovery and validates the local CLI discovery path on every pull request.

skills.sh is treated as a **discovery/install adapter**, not as another runtime source. Its eventual retirement requires equivalent practical discovery/install reach, not merely the existence of `plugin.json`. That decision is tracked in `svg153/skills#34`.

## Agent Plugins 1.0 package

The portable package is rooted at the repository root:

```text
plugin.json
skills/
  github-build-or-reuse/
    SKILL.md
```

Agent Plugins 1.0 discovers skills from the fixed `skills/` location. `plugin.json` therefore contains only portable manifest metadata and does not duplicate a `skills` path field.

### Optional MCP composition

Agent Plugins can also discover a root `mcp.json`. That file is a **connection/launch contract**, not proof that the plugin repository implements the MCP server itself.

A conforming plugin may reuse:

- an existing remote MCP server via `streamable-http`;
- an existing executable via `stdio`;
- legacy `sse` where compatibility requires it.

Agent Plugins 1.0 does not define package-manager resolution of MCP dependencies by package name. It also does not define portable OAuth credential references. Authentication is client-managed, and plugin source must not embed secrets in HTTP headers.

The general reusable MCP composition model is tracked in `svg153/skills#35`; the planning multi-MCP pilot is `svg153/skills#36`.

### Why this package currently has no `mcp.json`

`github-build-or-reuse` can collect GitHub evidence through host-native GitHub access, the official/existing GitHub MCP Server, authenticated `gh`, the GitHub API, or web research. Making one of these paths mandatory would reduce portability without adding a unique capability.

Therefore the absence of `mcp.json` here means **no mandatory MCP dependency for this capability**, not “Agent Plugins should not reuse external MCPs”. A bespoke GitHub-wrapper MCP remains unjustified unless a differentiating capability gap appears.

## Compatibility evidence matrix

Compatibility claims are deliberately separated by evidence strength.

Last updated: 2026-09-07.

| Surface | Current evidence | Classification |
| --- | --- | --- |
| Agent Plugins 1.0 root package | fixed-layout + closed-field validation in CI | conformance/discovery verified |
| Agent Skills reference format | upstream `skills-ref validate` in CI | format verified |
| skills.sh / `npx skills` | `npx skills@latest add . --list` in CI | local install/discovery verified |
| GitHub CLI `gh skill` | `gh skill publish --dry-run` on runner GitHub CLI 2.98.0 | publish-path verified |
| GitHub Copilot CLI | `@github/copilot` 1.0.83, Node 22; marketplace add/browse/install/list in CI | Agent Plugin marketplace install/discovery verified |
| OpenAI Codex CLI | `@openai/codex` 0.153.4, Node 22, isolated `CODEX_HOME`; marketplace add + `plugin add` + installed/enabled state in CI | native Agent Plugin install/discovery verified |
| Codex generated adapter | still generated from canonical distribution config | compatibility fallback; retirement candidate after behavioral/update parity |
| Claude Code adapter | generated from canonical distribution config | manifest compatibility; runtime verification pending |
| Cursor adapter | generated from canonical distribution config | manifest compatibility; runtime verification pending |
| Gemini CLI adapter | generated from canonical distribution config | manifest compatibility; runtime verification pending |
| GitHub Agentic Workflows | no runtime evidence captured yet | pending |

Do not rewrite an **install/discovery** result as behavioral execution. Runtime claims should include client/version/date and the command or evidence used to verify them.

### Copilot CLI evidence

CI verifies the marketplace-first route with:

```bash
copilot plugin marketplace add .
copilot plugin marketplace browse github-build-or-reuse
copilot plugin install github-build-or-reuse@github-build-or-reuse
copilot plugin list
```

Observed on Copilot CLI 1.0.83:

- marketplace registration succeeds;
- `github-build-or-reuse` is discoverable;
- the plugin installs successfully with **1 skill**;
- `github-build-or-reuse@github-build-or-reuse` is enabled and loaded from the checked-out repository marketplace.

The marketplace path is intentionally preferred over direct repo/path installation because current Copilot CLI warns that direct plugin installs are deprecated.

### Codex CLI evidence

CI verifies the existing repo-local `.agents/plugins/marketplace.json` with an isolated `CODEX_HOME`:

```bash
codex plugin marketplace add .
codex plugin list --available --json
codex plugin add github-build-or-reuse@github-community-spain --json
codex plugin list --json
```

Observed on Codex CLI 0.153.4:

- marketplace `github-community-spain` registers from the repository;
- `github-build-or-reuse@github-community-spain` is available;
- installation resolves the root Agent Plugins package to version `1.2.2`;
- the installed plugin is cached under the isolated Codex plugin cache;
- final state reports `installed: true` and `enabled: true`.

This is native Agent Plugins evidence for the repository root. It does **not** yet prove that every behavior/evaluation path is identical to the generated `.codex-plugin` fallback or that update/governance semantics have full parity, so the generated Codex adapter is not removed by this change.

## Host-specific adapters

`.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/`, `marketplace.json`, and `gemini-extension.json` are compatibility/distribution outputs generated from canonical state. They must not become independent runtime copies.

The intended migration is to retire these surfaces **individually** when the corresponding client has Agent Plugin-native parity for installation, discovery, updates and runtime. Do not delete them as a batch merely because the portable manifest exists.

Codex is now the first host for which native Agent Plugin install/discovery parity is verified in CI. Its generated adapter is therefore a **retirement candidate**, not yet retired: behavioral invocation and update/governance parity should be captured first.

Regenerate and check adapters with:

```bash
python scripts/generate-distribution.py
python scripts/generate-distribution.py --check
```

## Security baseline

A distributable change must preserve these properties:

- no secrets or credentials in plugin metadata or `mcp.json`;
- portable `plugin.json` only uses Agent Plugins v1 fields;
- any `mcp.json` matches the same Agent Plugins specification version;
- remote MCP endpoints use a reviewed HTTPS origin and no embedded credential header;
- referenced skill content stays inside the repository package;
- external Actions remain full-SHA pinned with explicit permissions and timeouts;
- no custom MCP implementation is added without a concrete capability requirement;
- existing third-party MCP composition is allowed when it is part of the capability contract and has provenance/security review;
- license/provenance information remains intact;
- runtime compatibility is stated at the evidence level actually verified.
