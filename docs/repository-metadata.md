# GitHub repository metadata

Most repository metadata lives outside Git, but this project keeps its desired state documented and reproducible.

Apply the settings from an authenticated GitHub CLI session with repository `Administration: write`:

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

The script also keeps GitHub's native `delete branch on merge` setting enabled. The cleanup workflow remains defense in depth for stale branches.
