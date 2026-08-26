# skills.sh indexing

`github-build-or-reuse` is packaged for the Vercel `skills` CLI and validated in CI. Public skills.sh search ingestion is controlled by the external skills.sh service and can lag behind direct CLI discovery.

## Verified install/discovery

```bash
# Discover the skill directly from the public repository
npx -y skills@latest add ghspain/github-build-or-reuse --list

# Install only this skill
npx -y skills@latest add ghspain/github-build-or-reuse \
  --skill github-build-or-reuse
```

Repository CI also runs the equivalent local discovery command with telemetry disabled so validation does not manufacture install counts.

The repository includes `skills.sh.json`, but that manifest is presentation/grouping metadata; it is not a guarantee that the external skills.sh search index has crawled the repository.

## Indexing status

- Source repository: `ghspain/github-build-or-reuse`
- Canonical skill: `skills/github-build-or-reuse/SKILL.md`
- Source of truth: this repository
- Direct `npx skills` discovery: validated
- skills.sh search/index: external ingestion pending verification

Do not generate artificial installs to influence the directory. If direct installation works but search remains absent, request a crawl/re-index from `vercel-labs/skills`.

## Prepared upstream issue

**Title**

```text
[Listing]: Index ghspain/github-build-or-reuse
```

**Body**

```markdown
## Summary

Please index `ghspain/github-build-or-reuse` so its Agent Skill becomes discoverable through skills.sh and `npx skills find`.

Repository: https://github.com/ghspain/github-build-or-reuse
Skill: `github-build-or-reuse`
Canonical path: `skills/github-build-or-reuse/SKILL.md`

## Verified

- The repository is public.
- The skill uses the standard `skills/<name>/SKILL.md` layout and valid `name` / `description` frontmatter.
- The repository includes a root `skills.sh.json` grouping manifest.
- CI validates the Agent Skills specification, GitHub skill publishing, and current Vercel CLI discovery.

Direct discovery:

```bash
npx -y skills@latest add ghspain/github-build-or-reuse --list
```

Direct install:

```bash
npx -y skills@latest add ghspain/github-build-or-reuse --skill github-build-or-reuse
```

Direct CLI discovery is correct; if the repository is still absent from public search, this appears to be an indexing/ingestion gap rather than a repository-format problem. Could you please crawl/re-index it?
```

## After indexing

Once the repository page is confirmed live, add the skills.sh badge to the README. Do not add the badge while the directory returns `not found`/inaccessible, because that would present a broken state as project metadata.
