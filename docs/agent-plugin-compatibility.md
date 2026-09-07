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

skills.sh is treated as a **discovery/install adapter**, not as another runtime source. Its eventual retirement requires equivalent practical discovery/install reach, not merely the existence of `plugin.json`. The catalog-level retirement policy is recorded in `svg153/skills#34`.

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

## Evidence levels

Compatibility claims are deliberately separated by strength:

- **conformance** — deterministic package/schema/path validation;
- **install/discovery verified** — a named client/version validates or installs the package and reports it as available/installed;
- **compile/consumption verified** — an orchestration layer resolves the plugin and generates runnable host configuration;
- **behavioral runtime verified** — a real model/session activates the capability and executes representative behavior;
- **documented native support** — the vendor documents support, but this repository has not executed the client path itself.

Do not promote a lower evidence level to a stronger claim.

## Compatibility evidence matrix

Last updated: 2026-09-07.

| Surface | Version / environment | Current evidence | Classification |
| --- | --- | --- | --- |
| Agent Plugins 1.0 root package | Agent Plugins 1.0.0 | fixed-layout + closed-field validation in CI | `conformance` ✅ |
| Agent Skills reference format | pinned upstream `skills-ref` | canonical skill validates in CI | `conformance` ✅ |
| skills.sh / `npx skills` | `skills@latest`, telemetry disabled | canonical skill discovered from repository root | `install/discovery verified` ✅ |
| GitHub CLI `gh skill` | GitHub CLI 2.98.0 | `gh skill publish --dry-run` succeeds | publish path verified ✅ |
| GitHub Copilot CLI | `@github/copilot` 1.0.83, Node 22 | repository marketplace add/browse/install/list; plugin enabled | `install/discovery verified` ✅ |
| OpenAI Codex CLI | `@openai/codex` 0.153.4, Node 22, isolated `CODEX_HOME` | native Agent Plugin marketplace add/install/list; `installed: true`, `enabled: true` | `install/discovery verified` ✅ |
| Claude Code | `@anthropic-ai/claude-code` 2.1.263, Node 22, isolated `HOME` | strict plugin validation + local marketplace add + install + list | `install/discovery verified` ✅ |
| Gemini CLI | `@google/gemini-cli` 0.58.0, Node 22, isolated `HOME` | extension validate + local install + list; installed tree retains canonical `SKILL.md` | `install/discovery verified` ✅ |
| GitHub Agentic Workflows | `gh-aw` 0.88.4 | experimental `plugins:` workflow compiles; `v1.2.2` resolves to commit `74f8cfeca5c0ed5799a0ab71be88d06fc9e2afb1` in generated lock | `compile/consumption verified` ✅ |
| Cursor | current Agent Plugins-capable client/docs | vendor documents that conforming Agent Plugins load without changes; no headless repo-local install run captured here | documented native support; repository execution pending |
| Codex generated adapter | generated from canonical distribution config | still retained although native root Agent Plugin installation is verified | compatibility fallback; retirement candidate |

No row above claims model-driven behavioral execution. That stronger gate remains separate from package/install compatibility.

## Client evidence

### GitHub Copilot CLI

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
- the plugin installs successfully with one skill;
- `github-build-or-reuse@github-build-or-reuse` is enabled and loaded from the checked-out repository marketplace.

The marketplace path is intentionally preferred over direct repo/path installation because current Copilot CLI warns that direct plugin installs are deprecated.

### OpenAI Codex CLI

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

This is native Agent Plugins evidence for the repository root. It does **not** yet prove that every behavior/evaluation path is identical to the generated `.codex-plugin` fallback or that update/governance semantics have full parity.

### Claude Code

CI pins Claude Code 2.1.263 and uses an isolated home directory:

```bash
claude plugin validate . --strict
claude plugin marketplace add ./ --scope user
claude plugin list --available --json
claude plugin install github-build-or-reuse@github-build-or-reuse --scope user
claude plugin list --json
```

The first real-client validation exposed that the shared host manifest included an `interface` object that Claude ignores. The generator was corrected to omit that host-irrelevant field from `.claude-plugin/plugin.json` while keeping all runtime behavior in the canonical skill. Strict validation and installation then passed.

This is an important packaging rule: **derived adapters may share canonical state, but should emit only fields understood by their target host rather than one catch-all host manifest**.

### Gemini CLI

CI pins Gemini CLI 0.58.0 and uses an isolated home directory with Folder Trust disabled only inside that ephemeral test home so extension management cannot block on interactive trust prompts:

```bash
gemini extensions validate <repository-root>
gemini extensions install <repository-root> --consent --skip-settings
gemini extensions list
```

The check requires `github-build-or-reuse` to appear in the installed extension list and verifies that the installed extension contains:

```text
skills/github-build-or-reuse/SKILL.md
```

That proves the generated Gemini extension keeps the same canonical Agent Skill rather than introducing a second runtime copy.

### GitHub Agentic Workflows

CI pins `github/gh-aw` v0.88.4 through the exact setup-action commit and compiles a minimal workflow containing:

```yaml
engine: copilot
plugins:
  - ghspain/github-build-or-reuse@v1.2.2
```

The compiler currently marks `plugins` as experimental. The generated lock workflow must contain both the repository and the exact commit behind `v1.2.2`:

```text
74f8cfeca5c0ed5799a0ab71be88d06fc9e2afb1
```

This demonstrates plugin **consumption and immutable ref resolution at compile time**. It does not execute a model or claim end-to-end behavior.

### Cursor

Cursor currently documents native Agent Plugins support, including the standard root `plugin.json`, skills, and MCP components. Its documented local-development path is UI/reload based rather than a headless plugin-install command suitable for this CI gate.

Therefore this repository records Cursor as **vendor-native support documented; repository runtime/install not executed** instead of converting documentation into a false runtime claim.

## Host-specific adapters

`.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/`, `marketplace.json`, and `gemini-extension.json` are compatibility/distribution outputs generated from canonical state. They must not become independent runtime copies.

The intended migration is to retire these surfaces **individually** when the corresponding client has Agent Plugin-native parity for installation, discovery, updates and runtime. Do not delete them as a batch merely because the portable manifest exists.

Codex is the clearest current retirement candidate because native root Agent Plugin install/discovery is verified. Behavioral invocation plus update/governance parity should be captured before removing the fallback. Claude and Gemini now also have concrete adapter install/discovery evidence, but that does not by itself prove their adapters are unnecessary because their current install paths are still host-specific.

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
- compatibility is stated at the evidence level actually verified.
