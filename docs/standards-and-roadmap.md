# Standards, packaging and roadmap

This project deliberately separates **portable behavior** from **platform packaging**.

## Portable core: Agent Skills

The canonical skill lives at `skills/github-build-or-reuse/`. It follows the open Agent Skills specification: a directory named after the skill, a `SKILL.md` with YAML frontmatter, and optional references, examples, scripts and evals. This is the source that Agent Skills-compatible clients should consume.

## OpenAI packaging: plugin

OpenAI plugins can bundle skills and, when needed, MCP servers. The repository therefore includes `.codex-plugin/plugin.json` and a repo marketplace entry under `.agents/plugins/marketplace.json`. The plugin currently contains the skill only.

That is intentional: OpenAI's architecture recommends starting with the smallest shape that solves the workflow. This skill already works with host-provided GitHub connectors, APIs, web research or `gh`; another GitHub wrapper would add maintenance and authentication surface without creating new capability.

## GitHub Copilot

GitHub Copilot supports the Agent Skills standard across the cloud agent, code review, Copilot CLI, the Copilot app and agent mode in supported IDEs. GitHub CLI 2.90+ also provides `gh skill` commands to preview, install, update and publish skills from GitHub repositories. This repository keeps the canonical skill in a layout that can be installed directly rather than maintaining a Copilot-specific copy.

## AGENTS.md

`AGENTS.md` is repository-level guidance for coding agents working **on this project**. It is not the end-user skill and does not replace `SKILL.md`. Keep contributor/maintenance instructions in `AGENTS.md`; keep runtime workflow behavior in the skill.

## OpenAI Agent definitions

OpenAI Agents SDK “agent definitions” are programmatic `Agent(...)` configurations that combine instructions, models, tools, guardrails, handoffs and MCP integrations. They are not a portable replacement for a `SKILL.md` file. Add an Agents SDK example only if this repository later ships an executable service or reference application that owns an agent runtime.

## MCP decision

### Current verdict: do not bundle a custom MCP server

The workflow needs GitHub discovery and repository evidence, not a novel protocol or proprietary data source. Prefer, in order:

1. the host's native GitHub connector/API;
2. an existing GitHub MCP integration when the host supports it;
3. authenticated `gh` or GitHub API;
4. web research as fallback/context.

Building a bespoke MCP server that merely mirrors GitHub would contradict the project's own reuse principle.

### Reconsider MCP when

- the skill needs a stable cross-host GitHub tool contract that clients cannot otherwise provide;
- we need server-side aggregation/scoring that is expensive or unreliable in prompt logic;
- we add organization-specific/private data or workflows requiring centralized auth/policy;
- an existing MCP server cannot satisfy the requirement.

If that point arrives, evaluate existing GitHub MCP servers before building a new one.

## Future iterations

1. Run output evals and trigger evals across multiple hosts; optimize the description rather than assuming it triggers correctly.
2. Add release automation and publish tagged versions installable through `gh skill`.
3. Test the OpenAI plugin marketplace path in ChatGPT/Codex and prepare public-directory submission metadata if usage justifies it.
4. Add more worked decision cases (developer portals, feature flags, RAG stacks, self-hosted apps, internal tools).
5. Consider structured machine-readable decision output for CI/agent orchestration.
6. Consider MCP only after a real tool gap is demonstrated.
