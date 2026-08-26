#!/usr/bin/env bash
# Apply GitHub repository settings that require Administration: write.
set -euo pipefail

repo="${1:-ghspain/github-build-or-reuse}"

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: GitHub CLI (gh) is required." >&2
  exit 1
fi

gh auth status >/dev/null

echo "Configuring $repo"
gh repo edit "$repo" \
  --description "Agent Skill and ChatGPT/Codex plugin that searches before you build and decides USE, CONTRIBUTE, FORK, or BUILD" \
  --delete-branch-on-merge \
  --add-topic agent-skills \
  --add-topic skills-sh \
  --add-topic ai-agents \
  --add-topic github \
  --add-topic open-source \
  --add-topic software-reuse \
  --add-topic build-vs-buy \
  --add-topic due-diligence \
  --add-topic codex \
  --add-topic chatgpt \
  --add-topic github-copilot \
  --add-topic claude-code \
  --add-topic github-cli \
  --add-topic software-architecture

echo "Result:"
gh repo view "$repo" --json description,deleteBranchOnMerge,repositoryTopics \
  --jq '{description, deleteBranchOnMerge, topics: [.repositoryTopics[].name]}'
