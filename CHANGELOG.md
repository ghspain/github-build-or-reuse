# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

### Added

- `npx skills` / skills.sh installation and discovery documentation.
- `skills.sh.json` catalog metadata.
- CI coverage for Vercel `skills` CLI discovery with telemetry disabled.
- Automatic cleanup of same-repository branches after merged pull requests.
- Evidence-backed README demo with a dated public-repository snapshot in `assets/demo.json`.
- Dependency-free demo generator that deterministically produces the README SVG and Asciinema recording from one source of truth.
- CI drift detection for generated demo assets and an animated-GIF rendering workflow that reuses a pinned, checksum-verified `asciinema/agg` release.

### Changed

- Repository validation now derives the authoritative semantic version from `metadata.yaml` and verifies consistency across the canonical skill, plugin manifest, changelog, release notes, lifecycle files, labels and evals instead of hardcoding a release number.
- README demo now uses the existing AI presentation-generator scenario and real public evidence instead of an illustrative fictional result.

## [1.1.0] - 2026-08-25

### Added

- OpenAI skill-only plugin packaging and Git-backed marketplace entry.
- Canonical Agent Skills layout under `skills/github-build-or-reuse/`.
- Output evals and trigger-query eval set.
- Cross-client installation guidance including `gh skill` and GitHub Copilot.
- Standards/roadmap documentation covering Agent Skills, plugins, AGENTS.md, Agents SDK definitions and MCP.
- Repository SEO/settings recommendations.

### Changed

- Strengthened activation boundaries for tiny tasks and explicit no-discovery requests.
- Added candidate-repository prompt-injection/untrusted-input guidance.
- Made GitHub Community Spain the project publisher and lifecycle owner.

## [1.0.0] - 2026-08-25

### Added

- Concept-level GitHub discovery workflow.
- Evidence-based repository due diligence.
- Hard gates for functional, license, security, platform, maintenance and governance risk.
- Weighted comparison framework.
- Explicit `USE`, `CONTRIBUTE`, `FORK`, or `BUILD` verdict.
- GitHub CLI evidence playbook and licensing triage reference.
- Worked AI presentation-generator example.
