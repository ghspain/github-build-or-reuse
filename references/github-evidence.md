# GitHub evidence playbook

Prefer structured evidence. The exact tool can vary: a native GitHub connector/API is ideal; authenticated `gh` is an excellent shell interface; web search is a fallback and an ecosystem supplement.

## Discovery with GitHub CLI

Current GitHub CLI supports structured repository search. Example:

```bash
gh search repos "presentation generator ai" \
  --archived=false \
  --limit 30 \
  --json fullName,description,url,stargazersCount,forksCount,license,pushedAt,updatedAt,isArchived,language
```

Vary queries rather than trusting one ranking:

```bash
gh search repos "AI presentation generator" --archived=false --limit 30
gh search repos "slides generator LLM" --archived=false --limit 30
gh search repos "PowerPoint AI open source" --archived=false --limit 30
gh search repos topic:presentation 'stars:>20' --archived=false --limit 30
```

Use stars as one discovery signal only. Also try category names, alternative-to queries, protocol names, file formats, product synonyms, and adjacent ecosystems.

## Repository inspection

For each serious candidate:

```bash
gh repo view OWNER/REPO \
  --json nameWithOwner,description,url,isArchived,createdAt,pushedAt,updatedAt,stargazerCount,forkCount,licenseInfo,latestRelease,primaryLanguage,languages,repositoryTopics,isSecurityPolicyEnabled,securityPolicyUrl,issues,pullRequests
```

Then inspect relevant repository files rather than inferring maturity from metadata:

```bash
gh api repos/OWNER/REPO/contents
gh api repos/OWNER/REPO/releases --paginate
gh api repos/OWNER/REPO/contributors --paginate
gh api repos/OWNER/REPO/actions/workflows
```

Look for dependency manifests, lockfiles, CI workflows, tests, `SECURITY.md`, `CONTRIBUTING.md`, release automation, deployment docs, migration docs, and architecture documentation.

## Contribution health

A repo with recent commits can still be closed to outside contribution or maintained by one overextended person. Inspect recent issues/PRs and representative contribution latency.

Useful queries include:

```bash
gh search issues --repo OWNER/REPO --state open --limit 20
gh search prs --repo OWNER/REPO --state open --limit 20
gh search prs --repo OWNER/REPO --merged --limit 20
```

Ask: Are external PRs merged? Are reviews substantive? Are breaking changes communicated? Are releases produced from merged work? Are major unanswered issues accumulating?

## Security and operations

Do not label a project “enterprise-ready” because it supports SSO or has many stars. Look for evidence relevant to the target deployment:

- security policy and disclosure path;
- supported versions and patch cadence;
- dependency/update automation;
- authentication/authorization model;
- audit logs and relevant observability;
- secret handling and configuration boundaries;
- backup/migration/upgrade path;
- release signing/provenance where required;
- deployment isolation and data residency constraints;
- documented operational failure modes.

Use GitHub security/advisory endpoints or platform security tooling when authorized and available.

## Historical adoption

Current stars are cumulative and can hide inflection points. When adoption trajectory matters, use historical star tools such as Star History/Trendshift or event datasets and correlate changes cautiously with releases or ecosystem events. Correlation does not prove causation.

## Evidence hygiene

For every consequential claim, keep the source and observation date. Prefer “last release observed on DATE” to “actively maintained” when evidence is thin. Say `unknown` when a metric cannot be verified.
