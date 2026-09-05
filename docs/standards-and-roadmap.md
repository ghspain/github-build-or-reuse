# Standards, packaging and roadmap

This project deliberately separates **portable behavior** from **capability packaging and distribution**.

## Portable core: Agent Skills

The canonical skill lives at `skills/github-build-or-reuse/`. It follows the open Agent Skills specification: a directory named after the skill, a `SKILL.md` with YAML frontmatter, and optional references, examples, scripts and evals. This remains the source of portable runtime behavior even if Agent Plugins becomes the preferred package boundary.

The canonical path and skill identity are also compatibility invariants for skills.sh. Agent Plugins adoption must not move, rename or duplicate this runtime source as an incidental packaging change.

## Portable package: Agent Plugins 1.0

The repository root is also a portable Agent Plugins 1.0 package:

```text
plugin.json
skills/
  github-build-or-reuse/
    SKILL.md
```

Agent Plugins v1 discovers Agent Skills from the fixed `skills/` directory, so the existing Agent Skills / skills.sh layout is reused directly. `plugin.json` contains portable metadata only and does not duplicate a `skills` path field.

The intended direction is **plugin-first packaging with compatibility adapters**, not a second runtime implementation. An Agent Plugin may become the primary installable capability while `SKILL.md` remains its canonical behavior component.

During this pilot, `scripts/validate-agent-plugin.py` requires the skill set discovered by Agent Plugins to match the skill set registered in `skills.sh.json`. CI separately runs `npx skills@latest add . --list` and requires `github-build-or-reuse` to remain discoverable.

See [Agent Plugin compatibility and distribution contract](agent-plugin-compatibility.md) and [ADR 0001](adr/0001-agent-plugin-and-skills-sh-coexistence.md).

## Can Agent Plugins replace the other surfaces?

Potentially **some of them, over time**.

Agent Plugins is a package format for skills and MCP servers. It can remove the need for host-specific packaging adapters once a host consumes the standard natively with equivalent install, discovery, update and runtime behavior.

It does not make the Agent Skill disappear: the skill is a standard component inside the plugin. It also does not standardize public marketplaces or catalog ranking, so a discovery surface such as skills.sh still has independent value today.

Retirement policy therefore follows evidence, not file-count reduction:

1. Prefer Agent Plugins as the package boundary.
2. Keep `SKILL.md` as canonical behavior.
3. Retire host-specific generated adapters individually after native Agent Plugin parity is verified.
4. Keep skills.sh while it materially adds discovery/install reach.
5. Reassess skills.sh only after an equivalent Agent Plugin-native discovery path exists or skills.sh itself consumes Agent Plugins natively.

The detailed retirement criteria are tracked in `svg153/skills#34`.

## Derived cross-agent packaging

Platform manifests are generated from `distribution.config.json`, repository `metadata.yaml`, and the canonical `SKILL.md` identity/version. They are derived outputs rather than independent sources of truth.

```bash
python scripts/generate-distribution.py
python scripts/generate-distribution.py --check
```

The generated surfaces cover Agent Plugins, Codex, Claude Code, Cursor and Gemini. The richer standalone product metadata (branding, prompts, license, keywords and interface copy) stays in `distribution.config.json` so host manifests remain consistent without flattening the product to the catalog's generic defaults.

A generated adapter is evidence of **manifest compatibility**, not automatically runtime compatibility. Runtime claims must be backed by a client/version/date and install or execution evidence.

## GitHub Copilot

GitHub Copilot supports the Agent Skills standard across the cloud agent, code review, Copilot CLI, the Copilot app and agent mode in supported IDEs. GitHub CLI also provides `gh skill` commands in supporting versions. The canonical skill remains directly installable; no Copilot-specific runtime copy is maintained.

## skills.sh

`skills.sh.json` remains a supported public discovery surface. The repository protects the stable inputs under its control:

- repository identity `ghspain/github-build-or-reuse`;
- canonical skill name `github-build-or-reuse`;
- canonical path `skills/github-build-or-reuse/SKILL.md`;
- grouping registration in `skills.sh.json`;
- successful local `npx skills` discovery in CI.

External catalog indexing/ranking is not repository-controlled and is therefore not a blocking CI dependency. We protect the inputs rather than couple every PR to an external search index.

## AGENTS.md

`AGENTS.md` is repository-level guidance for coding agents working **on this project**. It is not the end-user skill and does not replace `SKILL.md`.

## Release and validation automation

Tagged releases are already automated by `.github/workflows/release.yml`; README demo assets are reproducibly regenerated by `render-demo.yml`; validation checks packaging, the Agent Plugin / skills.sh coexistence contract, Agent Skills conformance, generated-manifest drift and client discovery.

All repository workflows follow an enforced security baseline: external Actions are full-SHA pinned, checkout credentials do not persist, permissions are explicit, jobs have timeouts, and Dependabot tracks GitHub Actions updates.

## External discovery

### skills.sh Finder

The canonical skills.sh detail page and Finder entry are external distribution surfaces, not repository-owned indexes. Once the owner-scoped Finder returns `ghspain/github-build-or-reuse` with skill `github-build-or-reuse`, this repository treats catalog indexing as complete.

Exact-name discoverability and capability/semantic discoverability are separate concerns. The current legacy `skills find` client calls `skills.sh/api/search`; upstream behavior is known to match skill identity/source much more reliably than `SKILL.md` description text. Consequently, adding keyword stuffing to this repository is not considered a valid workaround for semantic search gaps. Capability search improvements belong upstream; see `vercel-labs/skills#1761`.

Repository metadata, README copy and skill frontmatter should still describe the capability clearly for GitHub search, web search, humans and future catalog implementations, but they must not be treated as proof that the current skills.sh Finder indexes description semantics.

Temporary discovery probes should be removed after owner-scoped indexing and exact-name discoverability are stable. A permanent CI dependency on an external catalog's ranking behavior would be noisy and outside this repository's control.

## MCP decision

### Agent Plugins MCP composition is broader than custom MCP implementation

Agent Plugins v1 optionally discovers MCP configuration from root `mcp.json`. That configuration may describe:

- an existing remote MCP server using `streamable-http`;
- an existing executable using `stdio`;
- legacy `sse` where compatibility requires it.

The MCP server therefore does **not** need to be implemented by the plugin repository. A capability can package its skills and declare existing third-party tool servers as part of the same installable contract.

Agent Plugins v1 does not define a package-manager dependency mechanism such as “install MCP package X by name”. It defines how a client connects to or launches each declared server. Authentication and credential storage are client-managed; credentials must not be committed in `mcp.json` headers.

Reusable MCP composition is tracked at catalog level in `svg153/skills#35`, with a multi-MCP planning pilot in `svg153/skills#36`.

### Current verdict for GitHub Build or Reuse: no mandatory `mcp.json`

The workflow needs GitHub discovery and repository evidence, but it deliberately supports several equivalent access paths. Prefer, in order according to the host:

1. the host's native GitHub connector/API;
2. the official/existing GitHub MCP integration when supported;
3. authenticated `gh` or GitHub API;
4. web research as fallback/context.

A bespoke GitHub wrapper would contradict the project's own reuse principle unless it creates a real capability unavailable through existing integrations.

Making the official GitHub MCP a mandatory `mcp.json` dependency would also narrow a skill that currently works through multiple host-native GitHub paths. Therefore this capability keeps `mcp.json` absent unless testing shows that a stable mandatory MCP contract improves behavior enough to justify the coupling.

This is a **capability-specific decision**, not a recommendation against MCP composition in Agent Plugins generally.

### Reconsider `mcp.json` here when

- a stable cross-host GitHub tool contract is unavailable elsewhere;
- runtime parity depends on one consistent GitHub tool surface;
- server-side aggregation/scoring becomes necessary;
- organization/private workflows require centralized auth or policy;
- an existing MCP supplies a required capability that host-native access cannot reliably provide.

## Future iterations

1. Promote behavioral evals to the repository's primary runtime quality gate and measure trigger/boundary behavior under a pinned executor.
2. Capture real install/runtime evidence for Codex, GitHub Copilot, GitHub Agentic Workflows, Claude Code, Cursor and Gemini and maintain the evidence classification in `docs/agent-plugin-compatibility.md`.
3. Feed this pilot into `svg153/skills#34` to decide which host-specific adapters can be retired safely.
4. Generalize optional third-party MCP composition through `svg153/skills#35`.
5. Prove skills + multiple reused MCP servers together with the planning pilot in `svg153/skills#36`.
6. Add more worked decision cases (developer portals, feature flags, RAG stacks, self-hosted apps, internal tools).
7. Consider structured machine-readable decision output for CI/agent orchestration.
