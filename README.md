# GitHub Build or Reuse

An agent skill for answering a question that should come before substantial implementation:

> Should we **USE**, **CONTRIBUTE**, **FORK**, or **BUILD**?

Modern coding agents make greenfield software cheap enough that teams can accidentally recreate mature open-source work before checking what already exists. This skill makes discovery and due diligence a first-class engineering gate.

## What is different

This is intentionally more than a GitHub repository search prompt. It separates four stages:

1. **Requirements** — define must-haves and hard constraints.
2. **Discovery** — find projects by product concept, not only exact library names.
3. **Due diligence** — inspect fit, maintenance, security, governance, licensing, architecture, CI/tests, releases, and contribution health.
4. **Decision** — recommend exactly one primary path: `USE`, `CONTRIBUTE`, `FORK`, or `BUILD`.

Popularity is evidence of attention, not proof of quality. A high star count never overrides a failed license, security, architecture, or must-have requirement gate.

## Tool strategy

The skill is tool-agnostic but prefers structured GitHub evidence when available:

1. Native GitHub connector/API.
2. Authenticated GitHub CLI (`gh`).
3. GitHub web pages and GitHub search.
4. Broader web search for ecosystem context, comparisons, historical adoption, or evidence GitHub does not expose directly.

See [`references/github-evidence.md`](references/github-evidence.md) for current `gh` examples.

## Decision model

The default weighted model is:

| Dimension | Weight |
| --- | ---: |
| Functional fit | 30 |
| Architecture & integration | 15 |
| Maintenance & project health | 15 |
| Security & operational readiness | 15 |
| License & governance | 10 |
| Community sustainability | 10 |
| Adoption/migration cost | 5 |

Scores are decision support, not an automatic verdict. Hard gates always win. See [`references/decision-framework.md`](references/decision-framework.md).

## Due-diligence depth

- **Quick scan** — discovery, license, archive/activity, README-level fit. Good for low-cost experiments.
- **Standard** — adds releases, CI/tests, security policy, issues/PRs, docs, architecture, contribution health. Default for a real implementation decision.
- **Deep** — adds code/dependency inspection, maintainer concentration, security history, PoC/benchmarking, upgrade/migration risk. Use for strategic or enterprise adoption.

## Example

See [`examples/presentation-generator.md`](examples/presentation-generator.md) for an example of turning “build an AI presentation app” into an evidence-driven reuse decision.

## Standalone-ready layout

This directory is intentionally structured as a future repository root. You can copy the **contents of this folder** into a new repository without relying on the parent skills monorepo.

```text
.
├── .github/workflows/validate.yml
├── agents/openai.yaml
├── examples/
├── references/
├── scripts/validate.py
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
├── SKILL.md
└── metadata.yaml
```

The nested `.github` workflow is inert while this project is stored inside another repository, and becomes a normal repository workflow after extraction to its own root.

## Validation

```bash
python scripts/validate.py
```

The validator uses only the Python standard library.

## Inspiration and attribution

The original trigger for this project was [`polmarza/github-repo-scout`](https://github.com/polmarza/github-repo-scout), an MIT-licensed skill built around searching GitHub by product concept, filtering licenses, and checking repository freshness. This project is an independent implementation that expands the idea into structured due diligence and a build-vs-reuse decision framework.

See [`NOTICE.md`](NOTICE.md).

## License

MIT.
