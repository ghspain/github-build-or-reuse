# Immutable release tags

The repository publishes versioned skill/plugin releases and recommends pinned installs such as `v1.2.2`. Those references should be immutable after publication.

## Reuse-first basis

GitHub maintains an official [`github/ruleset-recipes`](https://github.com/github/ruleset-recipes) repository. Its [`tag-rulesets/prevent-tag-delete.json`](https://github.com/github/ruleset-recipes/blob/main/tag-rulesets/prevent-tag-delete.json) recipe is the basis for this repository's rule.

The official recipe protects tags with:

- `deletion`;
- `non_fast_forward`.

This repository keeps those protections and adds only two intentional differences:

1. target only release tags matching `refs/tags/v*`, rather than every tag;
2. add GitHub's `update` rule so an existing release tag cannot be moved by an ordinary ref update either.

The tracked importable recipe is:

```text
.github/rulesets/immutable-release-tags.json
```

CI validates that it remains an active `tag` ruleset targeting exactly `refs/tags/v*`, with no default bypass actors and exactly these protections:

```text
delete blocked
update blocked
non-fast-forward blocked
```

Creation is deliberately **not** restricted: normal release automation/maintainers still need to create a new `vX.Y.Z` tag. The rule makes the tag immutable after creation.

## Why this is separate from CI

A repository ruleset is server-side repository policy. Committing the JSON does not activate it.

Creating or editing repository rulesets requires repository administration/ruleset-edit permission. The repository therefore does not store an admin token or grant GitHub Actions administration rights just to self-configure this setting.

The public ruleset endpoint can still be read to verify state. As of the issue that introduced this hardening, `GET /repos/ghspain/github-build-or-reuse/rulesets` returned an empty list, which matches the warning emitted by `gh skill publish --dry-run`.

## Apply in the GitHub UI

An administrator can use GitHub's native JSON import flow:

1. Open the repository **Settings**.
2. Open **Rules → Rulesets**.
3. Choose **New ruleset → Import a ruleset**.
4. Select `.github/rulesets/immutable-release-tags.json` from a local checkout.
5. Review the target (`v*`) and protections.
6. Create the ruleset with enforcement **Active**.

GitHub documents JSON import as the supported way to reuse a ruleset across repositories.

## Apply idempotently with GitHub CLI

The repository also includes an admin helper:

```bash
scripts/manage-release-ruleset.sh status
scripts/manage-release-ruleset.sh apply
```

`apply` is idempotent by ruleset name:

- if `Immutable release tags v*` does not exist, it uses the repository ruleset `POST` endpoint;
- if it already exists, it updates that ruleset in place with `PUT`;
- it then fetches the live ruleset for verification.

Use an authenticated `gh` context with repository **Administration: write** (or an equivalent custom role that can edit repository rules). Do not put that credential in this repository or in ordinary CI.

To target a fork/test repository while validating the helper:

```bash
GH_REPO=owner/test-repo scripts/manage-release-ruleset.sh apply
```

## Verify after activation

Run:

```bash
scripts/manage-release-ruleset.sh status
```

Then repeat:

```bash
gh skill publish --dry-run
```

The release-hardening issue is complete when the live repository has the active tag ruleset and the publisher no longer reports missing tag protection.

## Threat model / limits

This protects the **Git ref** used as a versioned install reference. It does not by itself provide artifact signing or provenance attestation. Those can be layered separately if the release workflow begins distributing additional build artifacts.

Avoid adding broad bypass actors. If an emergency requires changing a published version, prefer releasing a new version rather than moving an existing `v*` tag.
