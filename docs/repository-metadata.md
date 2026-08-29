# GitHub repository configuration

Repository configuration is managed as code wherever GitHub's permission model allows it.

The workflow `.github/workflows/repository-config.yml` is the repository configuration entry point:

- it reconciles labels from `.github/labels.json` with the standard `GITHUB_TOKEN`;
- it applies administrative repository settings through `scripts/configure-repository-settings.sh` when the `REPOSITORY_ADMIN_TOKEN` secret is available;
- it can also be run manually with `workflow_dispatch`.

The administrative token is intentionally separate because the standard Actions `GITHUB_TOKEN` does not provide the `Administration: write` permission required to update repository settings.

The same settings script can be run from an authenticated GitHub CLI session with repository `Administration: write`:

```bash
./scripts/configure-repository-settings.sh
```

## Description

> Agent Skill and ChatGPT/Codex plugin that searches before you build and decides USE, CONTRIBUTE, FORK, or BUILD.

## Topics

- `agent-skills`
- `skills-sh`
- `ai-agents`
- `github`
- `open-source`
- `software-reuse`
- `build-vs-buy`
- `due-diligence`
- `codex`
- `chatgpt`
- `github-copilot`
- `claude-code`
- `github-cli`
- `software-architecture`

The repository deliberately does not use `mcp` as a discovery topic because it does not ship an MCP server today. The title and README already contain the strongest search terms naturally; topics should describe actual capabilities rather than keyword-stuff the repository.

GitHub's native `delete branch on merge` setting is part of the desired repository settings. No cleanup workflow is needed: once the native setting is enabled, GitHub owns branch deletion after merges.
