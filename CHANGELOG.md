# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

## [1.2.1] - 2026-09-03

### Added

- Deterministic cross-agent distribution generation for Agent Plugins, Codex, Claude Code, Cursor, and Gemini from one standalone packaging configuration.
- Enforced GitHub Actions security baseline with immutable action SHAs, non-persisted checkout credentials, explicit permissions, job timeouts, and Dependabot coverage for Actions.
- Canonical top-level Waza behavioral suite with deterministic `spec verify` validation and trusted model-backed execution evidence.

### Changed

- Moved intrinsic behavioral ownership from legacy skill-local JSON eval fixtures to the canonical Waza suite under `evals/github-build-or-reuse/`.
- Updated packaging/standards documentation to reflect existing release automation and derived multi-agent manifests.

### Compatibility

- The runtime decision model and instructions are unchanged from 1.2.0; this patch release updates packaging, CI hardening, and behavioral evaluation infrastructure only.

## [1.2.0] - 2026-09-01

### Added

- `npx skills` / skills.sh installation and discovery documentation.
- `skills.sh.json` catalog metadata.
- CI coverage for Vercel `skills` CLI discovery with telemetry disabled.
- Automatic cleanup of same-repository branches after merged pull requests.
- Evidence-backed README demo with a dated public-repository snapshot in `assets/demo.json`.
- Dependency-free demo generator that deterministically produces the README SVG and Asciinema recording from one source of truth.
- CI drift detection for generated demo assets and an animated-GIF rendering workflow that reuses a pinned, checksum-verified `asciinema/agg` release.
- Original README banner and animated terminal demo focused on the reuse decision flow.

### Changed

- Broadened skill activation so common already-solved capabilities such as auth, payments, scraping, browser automation, notifications, search/RAG, observability, GitHub automation, media processing, queues, schedulers, rate limiting and workflow engines trigger discovery earlier.
- Added explicit rules to perform available due diligence for the user and never silently present degraded verification as equivalent evidence.
- Improved README product positioning, search-oriented language, examples, prompts and installation paths after reviewing related open-source work.
- Expanded repository/plugin discovery metadata around Agent Skills, GitHub Copilot, Codex, Claude Code, open-source alternatives and build-vs-open-source decisions.
- Repository validation now derives the authoritative semantic version from `metadata.yaml` and verifies consistency across the canonical skill, plugin manifest, changelog, release notes, lifecycle files, labels and evals instead of hardcoding a release number.
- README demo now uses the existing AI presentation-generator scenario and real public evidence instead of an illustrative fictional result.

### Fixed

- Animated demo rendering now stages generated assets before checking for changes, so a newly created GIF is committed instead of being missed as an untracked file.

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
