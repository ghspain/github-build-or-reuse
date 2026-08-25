# Example: AI presentation generator

## User intent

> I want to build an application that generates presentations with AI.

A weak workflow starts coding. A repository-scout workflow searches for matching repositories. This skill first turns the idea into a decision.

## Requirements snapshot

Assume the user clarifies that decks must remain editable, PPTX export matters, multiple LLM providers are desirable, self-hosting and commercial use are expected, and authentication, auditability, logging and reliable deployment will eventually matter.

## Discovery

Search multiple conceptual angles such as `AI presentation generator open source`, `LLM slides generator GitHub`, `PPTX AI generator`, `self hosted presentation AI`, known alternatives/forks and relevant GitHub topics. Do not stop at the first visually similar result.

## Shortlist evidence

For each serious candidate collect exact license, editable-output support, activity/releases, issue and PR health, tests/CI, architecture/provider abstraction, auth/security model, deployment path, extension model, and evidence that maintainers accept comparable external contributions.

## Decision examples

- **USE:** a candidate already covers the must-haves and only needs configuration or small extensions.
- **CONTRIBUTE:** a strong base lacks a bounded capability that fits upstream architecture and maintainers accept comparable contributions.
- **FORK:** a strong base saves substantial work but the desired product needs sustained divergence that upstream does not want; the license and ownership cost are acceptable.
- **BUILD:** available projects cannot support critical output, deployment, security or workflow requirements without replacing most core internals. Reuse mature components and implementation patterns where possible.

A good final answer begins with one verdict and confidence, shows the hard gates and evidence gaps, compares credible candidates, estimates adaptation versus greenfield effort, and proposes the smallest reversible next test.
