# GitHub Build or Reuse

**Search before you build.** A portable Agent Skill and ChatGPT/Codex plugin that researches existing GitHub and open-source projects before substantial implementation, then recommends one path: **USE, CONTRIBUTE, FORK, or BUILD**.

[![Validate](https://github.com/ghspain/github-build-or-reuse/actions/workflows/validate.yml/badge.svg)](https://github.com/ghspain/github-build-or-reuse/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/ghspain/github-build-or-reuse)](https://github.com/ghspain/github-build-or-reuse/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI coding agents have made greenfield software dramatically cheaper to produce. That makes a previously mundane engineering question more important, not less:

> **Does this need to be built at all?**

`github-build-or-reuse` turns that question into a repeatable pre-build gate. It searches by product concept rather than exact package name, verifies serious candidates, compares adoption with greenfield effort, and makes the reuse decision explicit.

## The four outcomes

| Decision | Meaning |
| --- | --- |
| **USE** | Adopt an existing project because it already clears the important requirements and risk gates. |
| **CONTRIBUTE** | Use a strong upstream and add the missing capability there rather than creating a parallel implementation. |
| **FORK** | Reuse a strong base but deliberately own sustained divergence, upgrades and security. |
| **BUILD** | Start greenfield because no candidate clears the hard gates or adaptation would replace the core anyway. |

Even `BUILD` should preserve reusable libraries, protocols, schemas and implementation lessons discovered during research.

## What it checks

The default due diligence goes beyond stars and README claims:

- functional requirement coverage;
- architecture, extension points and deployment fit;
- recent maintenance, releases, CI and issue/PR health;
- security policy, dependency hygiene, auth, auditability and observability when relevant;
- license and governance constraints;
- maintainer concentration and contribution sustainability;
- adoption, migration and long-term fork cost.

Hard gates override popularity and numeric scoring. Unknown evidence stays **unknown**.

## Install

### GitHub CLI / GitHub Copilot — recommended portable path

GitHub CLI **2.90.0+** can preview, install and update Agent Skills directly from GitHub repositories:

```bash
# Inspect before installing
gh skill preview ghspain/github-build-or-reuse github-build-or-reuse

# Install the current version
gh skill install ghspain/github-build-or-reuse github-build-or-reuse

# Or install a reproducible release
gh skill install ghspain/github-build-or-reuse github-build-or-reuse@v1.1.0

# Later, check/update an unpinned installation
gh skill update github-build-or-reuse
```

For a long-lived environment, prefer a release tag or `--pin` so an upstream update cannot silently change behavior. GitHub Copilot supports Agent Skills in the cloud agent, code review, Copilot CLI, the Copilot app and agent mode in supported IDEs. `gh skill` can also target another supported agent host and scope; inspect `gh skill install --help` for the hosts available in your current CLI.

### ChatGPT / Codex plugin

This repository is also packaged as an OpenAI plugin. For the stable release in Codex CLI:

```bash
codex plugin marketplace add ghspain/github-build-or-reuse --ref v1.1.0
```

Use `--ref main` only when you intentionally want the latest development version. Then open `/plugins`, choose the **GitHub Community Spain** marketplace, install **GitHub Build or Reuse**, and start a new session. OpenAI plugins can bundle skills and MCP tools; this plugin intentionally bundles only the portable skill today.

### Skill-only install for Agent Skills-compatible clients

The canonical portable skill is:

```text
skills/github-build-or-reuse/
```

Copy or install that directory into the skill location supported by your client. Common project/user locations include `.agents/skills/` and `~/.agents/skills/`; GitHub Copilot also supports `.github/skills/` and `~/.copilot/skills/`.

For Claude Code, GitHub CLI can install a compatible skill directly for that host, for example:

```bash
gh skill install ghspain/github-build-or-reuse github-build-or-reuse@v1.1.0 --agent claude-code --scope user
```

## Use

You do not need a magic phrase. The skill description is designed to activate on substantial new-app/tool/feature decisions and open-source alternative searches. You can also invoke it explicitly:

> Before building this self-hosted service, search GitHub and decide whether we should USE, CONTRIBUTE, FORK, or BUILD.

Other useful prompts:

- “Is there already an open-source project that covers most of this?”
- “Compare these two repositories as a base for our product.”
- “Could we contribute the missing feature upstream instead of maintaining a fork?”
- “Prove that greenfield is the better option before we start generating code.”

Tiny throwaway scripts and mechanical edits intentionally do **not** require a full repository due-diligence cycle.

## How it works

1. **Frame requirements** — must-haves, constraints, deployment, security, licensing and acceptable adaptation effort.
2. **Discover by concept** — multiple queries, synonyms, alternatives, topics and adjacent ecosystems.
3. **Verify candidates** — structured GitHub/API/`gh` evidence where possible; web research as fallback/context.
4. **Apply hard gates** — functional, license, security, platform, maintenance and governance.
5. **Score fit** — functional fit carries the most weight; stars never decide the result.
6. **Compare reuse vs greenfield** — include migration, extension and long-term ownership cost.
7. **Choose one path** — USE, CONTRIBUTE, FORK or BUILD, with confidence and the smallest reversible next action.

See the [`decision framework`](skills/github-build-or-reuse/references/decision-framework.md) and the [`GitHub evidence playbook`](skills/github-build-or-reuse/references/github-evidence.md).

## Due-diligence depth

- **Quick** — concept search, license, archive/activity and README-level fit for low-cost experiments.
- **Standard** — adds releases, tests/CI, security policy, issues/PRs, architecture and contribution health. Default for a real adoption decision.
- **Deep** — adds code/dependency inspection, maintainer concentration, security history, PoC/benchmarks and upgrade/migration risk for strategic adoption.

## Why there is no bundled MCP server

Because the project follows its own rule: **reuse before build**.

The workflow already works with host-provided GitHub connectors/API, existing MCP integrations, authenticated `gh`, or web research. A bespoke MCP server that simply wraps GitHub would add authentication, maintenance and security surface without adding a unique capability.

We will reconsider MCP when there is a demonstrated cross-host tool gap or a need for server-side aggregation/policy. See [`docs/standards-and-roadmap.md`](docs/standards-and-roadmap.md).

## Standards and compatibility

The canonical skill follows the open **Agent Skills** specification. GitHub Copilot supports that standard across multiple surfaces, and the repository additionally follows OpenAI's plugin packaging conventions (`.codex-plugin/plugin.json` + `skills/`). `AGENTS.md` remains project-maintainer guidance rather than runtime skill content.

See [`docs/standards-and-roadmap.md`](docs/standards-and-roadmap.md) for the reasoning behind Agent Skills, plugins, AGENTS.md, OpenAI Agents SDK definitions and MCP.

## Quality and evals

The skill ships with output evals and trigger queries under [`skills/github-build-or-reuse/evals/`](skills/github-build-or-reuse/evals/). CI validates the repository structure and the skill against the Agent Skills reference validator.

```bash
python scripts/validate.py
```

## Project structure

```text
.
├── .agents/plugins/marketplace.json
├── .codex-plugin/plugin.json
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── labels.json
│   └── workflows/
├── docs/
│   └── releases/
├── skills/
│   └── github-build-or-reuse/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── evals/
│       ├── examples/
│       └── references/
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── LICENSE
├── NOTICE.md
├── README.md
└── SECURITY.md
```

## Inspiration

The project was prompted in part by [polmarza/github-repo-scout](https://github.com/polmarza/github-repo-scout), an MIT-licensed skill built around concept-level GitHub discovery, license filtering and repository freshness. `github-build-or-reuse` is an independent implementation that extends the idea into requirements, due diligence, enterprise/operational evidence and an explicit build-vs-reuse decision framework. See [`NOTICE.md`](NOTICE.md).

## Contributing and governance

Issues and pull requests are welcome. Please keep the portable runtime behavior in the canonical skill and platform packaging at repository root; see [`CONTRIBUTING.md`](CONTRIBUTING.md), [`GOVERNANCE.md`](GOVERNANCE.md), and [`AGENTS.md`](AGENTS.md).

## License

MIT © 2026 GitHub Community Spain.
