#!/usr/bin/env bash
set -euo pipefail

repo="${GH_REPO:-ghspain/github-build-or-reuse}"
ruleset_name="Immutable release tags v*"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ruleset_file="$root/.github/rulesets/immutable-release-tags.json"
mode="${1:-status}"

usage() {
  cat <<'EOF'
Usage: scripts/manage-release-ruleset.sh [status|apply]

Environment:
  GH_REPO  repository in owner/name form (default: ghspain/github-build-or-reuse)

Commands:
  status   show whether the named repository ruleset exists and its live details
  apply    create it when missing or update it in place when it already exists

`apply` requires a `gh` authentication context with repository Administration: write
(or an equivalent custom role that can edit repository rules).
EOF
}

case "$mode" in
  status|apply) ;;
  -h|--help|help)
    usage
    exit 0
    ;;
  *)
    echo "ERROR: unknown mode: $mode" >&2
    usage >&2
    exit 2
    ;;
esac

python "$root/scripts/validate-release-ruleset.py"
command -v gh >/dev/null 2>&1 || {
  echo "ERROR: GitHub CLI (gh) is required" >&2
  exit 2
}

ruleset_id="$(
  gh api "repos/$repo/rulesets" \
    --jq ".[] | select(.name == \"$ruleset_name\") | .id" \
    | head -n 1
)"

if [[ "$mode" == "status" ]]; then
  if [[ -z "$ruleset_id" ]]; then
    echo "MISSING: $ruleset_name is not configured on $repo"
    exit 1
  fi
  echo "FOUND: $ruleset_name (id=$ruleset_id)"
  gh api "repos/$repo/rulesets/$ruleset_id" \
    --jq '{name, target, enforcement, conditions, rules: [.rules[].type]}'
  exit 0
fi

if [[ -z "$ruleset_id" ]]; then
  echo "CREATE: $ruleset_name on $repo"
  gh api --method POST "repos/$repo/rulesets" \
    --input "$ruleset_file" \
    --jq '{id, name, target, enforcement}'
else
  echo "UPDATE: $ruleset_name on $repo (id=$ruleset_id)"
  gh api --method PUT "repos/$repo/rulesets/$ruleset_id" \
    --input "$ruleset_file" \
    --jq '{id, name, target, enforcement}'
fi

echo "VERIFY:"
"$0" status
