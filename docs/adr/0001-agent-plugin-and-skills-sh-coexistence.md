# ADR 0001: Agent Plugins complements Agent Skills and skills.sh

- Status: Accepted
- Date: 2026-09-04
- Issue: https://github.com/ghspain/github-build-or-reuse/issues/28
- Parent initiative: https://github.com/svg153/skills/issues/33

## Context

The repository already publishes a portable Agent Skill and several generated host-specific packaging surfaces. Agent Plugins 1.0 standardizes a portable plugin root with fixed discovery of Agent Skills from `skills/` and optional MCP servers from `mcp.json`.

The project is also already discoverable through the Agent Skills / skills.sh ecosystem. Replacing that layout with a plugin-specific copy would risk breaking existing installation paths and create two runtime sources of truth.

## Decision

1. `skills/github-build-or-reuse/SKILL.md` remains the only canonical runtime skill.
2. The repository root is also a conforming Agent Plugins 1.0 package through `plugin.json` plus the existing fixed `skills/` directory.
3. `skills.sh.json` remains a supported distribution surface. Agent Plugin adoption must not rename, move, or duplicate the canonical skill as an incidental packaging change.
4. CI enforces parity between the skills Agent Plugins discovers from `skills/*/SKILL.md` and the skills registered in `skills.sh.json`.
5. Host-specific manifests remain generated adapters and cannot override the portable runtime source.
6. No custom GitHub-wrapper MCP is bundled unless a future evidence-backed capability gap requires one. Existing native connectors, GitHub MCP integrations, `gh`, GitHub APIs, and web research are preferred.
7. Compatibility documentation must distinguish schema/manifest compatibility, install/discovery verification, and actual runtime verification.

## Consequences

### Positive

- Existing skills.sh and Agent Skills users retain the same repository, skill name, and canonical path.
- Agent Plugins-compatible clients can consume the repository without a second copy of the skill.
- Distribution drift becomes testable rather than a documentation convention.
- Future host adapters can be removed as clients converge on Agent Plugins without rewriting runtime behavior.

### Trade-offs

- External skills.sh indexing availability cannot be guaranteed by repository CI; only the stable repository inputs and local discovery path can be guaranteed.
- Some client-specific adapters remain necessary until those clients consume the portable package directly.
- Runtime compatibility still has to be tested per client; a valid manifest alone is not proof of equivalent execution.

## Rejected alternatives

### Move the skill into a plugin-only directory

Rejected because Agent Plugins already discovers the existing `skills/` layout and moving it would risk breaking skills.sh and Agent Skills consumers for no capability gain.

### Duplicate `SKILL.md` for every platform

Rejected because copies drift and make provenance, releases, fixes, and behavioral eval ownership ambiguous.

### Bundle a custom GitHub MCP immediately

Rejected because the project already has multiple ways to collect GitHub evidence and a wrapper would contradict the reuse-before-build principle without a demonstrated missing capability.
