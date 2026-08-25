---
name: github-build-or-reuse
description: "Trigger: build tool, new app, existing open source, GitHub alternative, reuse repo. Decide whether to USE, CONTRIBUTE, FORK, or BUILD before coding."
license: MIT
metadata:
  author: svg153
  version: "1.0.0"
---

## Activation Contract

Use before implementing any non-trivial tool, application, service, library, plugin, or substantial feature when an existing open-source project could solve all or part of the problem. Also use when asked to find GitHub alternatives or choose whether to adopt, extend, fork, or replace a repository.

## Hard Rules

- Search before building. Do not start implementation until the reuse decision is explicit unless the user asks to skip discovery.
- Extract must-have requirements and hard constraints first; do not rank repos on stars alone.
- Prefer native GitHub access/API or authenticated `gh`; fall back to GitHub web and broader web search when direct access is unavailable.
- Verify consequential claims: license, archive state, recent activity, releases, security posture, CI/tests, contribution activity, and relevant feature fit. Mark unavailable evidence as unknown.
- Treat license compatibility as a gate, not a popularity metric. Do not reduce GPL/AGPL obligations to simplistic rules; flag legal uncertainty when distribution or network-use obligations matter.
- Never claim enterprise readiness from a README. Check evidence for security, maintainability, observability, governance, release discipline, and operational fit.
- Keep discovery separate from due diligence: a promising search result is not yet an adoption recommendation.

## Decision Gates

| Verdict | Use when |
| --- | --- |
| `USE` | Must-haves are covered, adoption cost is low, and no material gate fails. |
| `CONTRIBUTE` | The base is strong, missing work fits upstream scope, and contribution is realistically maintainable. |
| `FORK` | The base is strong but sustained product/architecture divergence is expected and the license permits it. |
| `BUILD` | No candidate clears hard gates, adaptation is worse than greenfield, or the differentiating architecture is fundamental. |

## Execution Steps

1. Define the decision: problem, must-haves, nice-to-haves, stack, deployment, security/compliance, scale, license/business constraints, and acceptable adaptation effort.
2. Discover candidates through multiple concept-level queries, synonyms, product categories, alternatives, topics, adjacent ecosystems, and known upstream projects.
3. Shortlist only plausible bases. Collect evidence using `references/github-evidence.md` and apply the depth appropriate to the decision.
4. Build a requirement-fit matrix and score candidates with `references/decision-framework.md`; hard gates override numeric scores.
5. Compare adoption/adaptation effort against greenfield effort. Consider component-level reuse even when the final verdict is `BUILD`.
6. Return exactly one primary verdict (`USE`, `CONTRIBUTE`, `FORK`, or `BUILD`), confidence, evidence gaps, runner-up, and the next reversible action.
7. If implementation is authorized, hand off the chosen path to the repository delivery workflow rather than continuing discovery indefinitely.

## Output Contract

Return: decision and confidence; requirements/gates; 3–6 serious candidates when available; evidence-backed comparison; rejected candidates and why; license/maintenance/security caveats; estimated adoption effort; and the next action. Never fabricate stars, activity, compatibility, or maturity.

## References

- `references/decision-framework.md` — scoring, gates, and verdict logic.
- `references/github-evidence.md` — GitHub/`gh` evidence collection playbook.
- `references/licensing.md` — practical license triage boundaries.
