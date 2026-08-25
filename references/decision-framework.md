# Decision framework

Use this after discovery. Do not score obviously irrelevant repositories simply to fill a table.

## 1. Hard gates

Evaluate these before the weighted score. A failed hard gate can disqualify `USE` or `FORK` even when the numeric score is high.

- **Functional gate:** a non-negotiable capability is fundamentally absent or conflicts with the product model.
- **License gate:** intended use/distribution is incompatible or unresolved.
- **Security gate:** the architecture creates an unacceptable security boundary or unresolved critical risk.
- **Platform gate:** unsupported runtime, deployment model, data residency, hardware, protocol, or integration is non-negotiable.
- **Maintenance gate:** archived/dead project with no realistic ownership strategy when ongoing updates are required.
- **Governance gate:** upstream ownership or project direction is incompatible with the intended dependency risk.

Record a gate as `PASS`, `FAIL`, or `UNKNOWN`. Unknown is not pass.

## 2. Weighted score

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

### Rating anchors

- `0` — unusable or evidence contradicts requirement.
- `1` — major gaps; high risk or major rewrite.
- `2` — significant adaptation required.
- `3` — viable with meaningful work.
- `4` — strong fit; limited adaptation.
- `5` — excellent evidence-backed fit.

Do not fabricate decimal precision when evidence is qualitative.

## 3. Verdict logic

The score informs the verdict but does not determine it mechanically.

### USE

Choose when all hard gates pass, must-haves are already covered, adoption effort is low relative to greenfield, and future upgrades are manageable.

### CONTRIBUTE

Choose when the project is a strong base, the missing capability belongs naturally upstream, maintainers accept contributions, and carrying the change upstream is cheaper than owning a fork.

Check contribution guidelines and recent comparable PRs. A permissive contribution policy in a README is not evidence that a large architectural change will be accepted.

### FORK

Choose when the existing codebase saves substantial work but long-term divergence is expected. Confirm the license permits the intended use, estimate merge/upstream drift cost, identify which components will remain synchronized, and explicitly accept ownership of security/upgrades.

### BUILD

Choose when no candidate clears hard gates, adaptation requires rewriting core architecture, dependency/governance risk is unacceptable, or the differentiated behavior is itself the core product.

A `BUILD` verdict should still list reusable components, protocols, libraries, schemas, or implementation patterns discovered during research.

## 4. Confidence

Report `high`, `medium`, or `low` confidence based on evidence completeness, not rhetorical certainty.

- **High:** primary evidence covers the key gates and relevant code/operations were inspected.
- **Medium:** candidate fit is clear but some operational, contribution, or maintenance evidence is incomplete.
- **Low:** decision depends on unverified claims, missing code access, unclear licensing, or unknown requirements.

## 5. Sensitivity

Name the smallest fact that could flip the verdict. Examples: maintainer willingness to accept a plugin API, AGPL deployment implications, missing SSO support, unsupported database, or a PoC performance result.
