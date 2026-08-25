# Governance

GitHub Build or Reuse is maintained as a GitHub Community Spain open-source project.

## Scope

The project owns the reusable decision workflow that asks whether a non-trivial software request should **USE**, **CONTRIBUTE**, **FORK**, or **BUILD** after evidence-based open-source discovery and due diligence.

Platform-specific packaging may live in this repository when it makes the same canonical skill easier to install. Platform-specific behavior should not silently fork the core decision model.

## Source of truth

The canonical runtime skill is `skills/github-build-or-reuse/`. Documentation, plugin manifests, CI, release automation and community files live at repository root.

Downstream catalogs may mirror the canonical skill, but changes should be proposed upstream here first.

## Change policy

- Behavior changes should include or update evals when practical.
- New hard gates or scoring changes require evidence for the recurring problem they address.
- Client-specific packaging must not duplicate the canonical skill body.
- Security-sensitive changes receive deliberate human review.
- A custom MCP, executable agent, or hosted service should be added only when it provides a capability that existing tools do not already cover well.

## Releases

The version in `metadata.yaml` is authoritative for repository releases. Merging a new version with corresponding changelog/release notes triggers release automation. Semantic versioning is used pragmatically:

- patch: fixes and documentation/packaging corrections without meaningful behavior change;
- minor: backward-compatible skill behavior, decision-model, eval, or supported-client improvements;
- major: incompatible activation/output contract or decision semantics.

## Maintainers and contributions

GitHub Community Spain maintainers review pull requests and may delegate review to contributors with relevant domain knowledge. Contributions are welcome through issues and pull requests; see `CONTRIBUTING.md`.

The project favors transparent evidence and reversible decisions over popularity metrics or vendor-specific lock-in.
