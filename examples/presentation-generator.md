# Example: AI presentation generator

## User intent

> I want to build an application that generates presentations with AI.

A weak workflow starts coding. A repo-scout workflow searches for matching repositories. This skill first turns the idea into a decision.

## Requirements snapshot

Assume the user clarifies:

- Generates editable slide decks, not only images/PDFs.
- Supports PPTX export.
- Can use more than one LLM provider.
- Self-hosting is desirable.
- Commercial use is expected.
- Authentication, auditability, logging, and reliable deployment will eventually matter.
- The user is willing to contribute upstream if the base project is healthy.

## Discovery

Search multiple conceptual angles:

- `AI presentation generator open source`
- `LLM slides generator GitHub`
- `PPTX AI generator`
- `self hosted presentation AI`
- known commercial/open-source alternatives and their forks
- presentation/slides GitHub topics

Do not stop at the first repo that looks visually similar.

## Shortlist evidence

For each serious candidate collect:

- exact license and commercial-use implications;
- editable PPTX support versus image/PDF-only output;
- recent pushes and releases;
- issue/PR health;
- tests and CI;
- architecture and provider abstraction;
- auth/security model;
- deployment path;
- extension/plugin model;
- contribution policy and evidence that external PRs are accepted.

## Decision examples

### USE

A candidate covers PPTX, provider abstraction, self-hosting, and deployment requirements with healthy maintenance. Remaining gaps are configuration or small extensions.

### CONTRIBUTE

A strong candidate lacks one provider or an export option, but its architecture clearly supports plugins and maintainers regularly merge comparable external PRs.

### FORK

A strong base saves months of work, but the desired product needs a persistent workflow/data model that upstream explicitly does not want. The license permits the intended fork and the user accepts ongoing merge/security ownership.

### BUILD

Available projects generate slides but their core architecture cannot support editable PPTX, required deployment/security boundaries, or the intended workflow without replacing most of the internals.

Even here, `BUILD` should reuse mature component libraries and learned implementation patterns where licensing and fit allow it.

## Good final answer shape

1. `Verdict: CONTRIBUTE — medium confidence`
2. Why the leading candidate wins.
3. Hard gates and unknowns.
4. Comparison of 3–6 credible candidates.
5. What the leading project still lacks.
6. Estimated adoption/change effort versus greenfield.
7. The smallest next test: for example, a 2-hour PoC exporting a representative PPTX and adding one provider adapter.
