# Decision framework

Use this after discovery. Do not score obviously irrelevant repositories simply to fill a table.

## Hard gates

Evaluate these before the weighted score. A failed hard gate can disqualify `USE` or `FORK` even when the numeric score is high.

- **Functional:** a non-negotiable capability is fundamentally absent or conflicts with the product model.
- **License:** intended use or distribution is incompatible or unresolved.
- **Security:** the architecture creates an unacceptable security boundary or unresolved critical risk.
- **Platform:** unsupported runtime, deployment model, data residency, hardware, protocol or integration is non-negotiable.
- **Maintenance:** archived/dead project with no realistic ownership strategy when ongoing updates are required.
- **Governance:** upstream ownership or project direction is incompatible with the intended dependency risk.

Record each as `PASS`, `FAIL`, or `UNKNOWN`. Unknown is not pass.

## Weighted score

Default to 0–5 per dimension, then convert with the weights below. Adjust weights only when user constraints justify it and state the change.

| Dimension | Weight | What to inspect |
| --- | ---: | --- |
| Functional fit | 30 | Must-have coverage, extension points, actual behavior, missing features |
| Architecture & integration | 15 | Stack, APIs, modularity, deployment, data model, extensibility |
| Maintenance & project health | 15 | Recent commits, releases, upgrade cadence, CI, issue hygiene |
| Security & operational readiness | 15 | Security policy, dependency hygiene, auth, secrets, logging, observability, release controls |
| License & governance | 10 | SPDX/license text, commercial fit, CLA/DCO, ownership, roadmap control |
| Community sustainability | 10 | Contributors, maintainer concentration, PR responsiveness, ecosystem, forks |
| Adoption/migration cost | 5 | Setup, migration, customization, operational burden, learning curve |

Rating anchors: `0` unusable; `1` major gaps; `2` significant adaptation; `3` viable with meaningful work; `4` strong fit; `5` excellent evidence-backed fit. Avoid fake decimal precision.

## Verdict logic

### USE
Choose when all hard gates pass, must-haves are already covered, adoption effort is low relative to greenfield, and future upgrades are manageable.

### CONTRIBUTE
Choose when the project is a strong base, the missing capability belongs naturally upstream, maintainers accept comparable contributions, and carrying the change upstream is cheaper than owning a fork.

### FORK
Choose when the existing codebase saves substantial work but long-term divergence is expected. Confirm license fit, estimate upstream drift cost and explicitly accept ownership of security and upgrades.

### BUILD
Choose when no candidate clears hard gates, adaptation requires replacing core architecture, dependency/governance risk is unacceptable, or differentiated behavior is itself the core product. Still list reusable components, protocols, libraries, schemas or patterns discovered during research.

## Confidence and sensitivity

Report `high`, `medium`, or `low` confidence based on evidence completeness rather than rhetorical certainty. Name the smallest missing fact or experiment that could flip the verdict.
