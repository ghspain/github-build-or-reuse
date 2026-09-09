#!/usr/bin/env bash
set -euo pipefail

PLUGIN_NAME="github-build-or-reuse"
MARKETPLACE_NAME="github-build-or-reuse-lifecycle"
REPOSITORY="ghspain/github-build-or-reuse"
OLD_VERSION="1.2.2"
OLD_REF="v1.2.2"
OLD_SHA="74f8cfeca5c0ed5799a0ab71be88d06fc9e2afb1"
NEW_VERSION="1.2.3"
NEW_REF="v1.2.3"
NEW_SHA="24af1931681bb03b0282472c4d4b6900359418c7"

if ! command -v copilot >/dev/null 2>&1; then
  echo "ERROR: copilot CLI is required" >&2
  exit 2
fi

SANDBOX="$(mktemp -d)"
trap 'rm -rf "$SANDBOX"' EXIT
MARKETPLACE_ROOT="$SANDBOX/marketplace"
TEST_HOME="$SANDBOX/home"
mkdir -p "$MARKETPLACE_ROOT" "$TEST_HOME/.copilot" "$SANDBOX/cache"

export HOME="$TEST_HOME"
export COPILOT_HOME="$TEST_HOME/.copilot"
export COPILOT_CACHE_HOME="$SANDBOX/cache"
export COPILOT_AUTO_UPDATE="false"

write_marketplace() {
  local version="$1"
  local ref="$2"
  local sha="$3"
  cat > "$MARKETPLACE_ROOT/marketplace.json" <<JSON
{
  "name": "$MARKETPLACE_NAME",
  "owner": {
    "name": "GitHub Community Spain"
  },
  "metadata": {
    "description": "Ephemeral lifecycle verification marketplace"
  },
  "plugins": [
    {
      "name": "$PLUGIN_NAME",
      "description": "Lifecycle verification for the portable Agent Plugin",
      "version": "$version",
      "source": {
        "source": "github",
        "repo": "$REPOSITORY",
        "ref": "$ref",
        "sha": "$sha"
      }
    }
  ]
}
JSON
}

assert_installed_version() {
  local expected="$1"
  local output="$SANDBOX/plugins-$expected.txt"
  copilot plugin list 2>&1 | tee "$output"
  grep -Fq "$PLUGIN_NAME@$MARKETPLACE_NAME" "$output"
  grep -Fq "(v$expected)" "$output"
}

assert_installed_skill() {
  local expected="$1"
  local skill_file
  skill_file="$(find "$COPILOT_HOME" -type f -path "*/skills/$PLUGIN_NAME/SKILL.md" -print -quit)"
  if [[ -z "$skill_file" ]]; then
    echo "ERROR: installed canonical SKILL.md was not found below $COPILOT_HOME" >&2
    find "$COPILOT_HOME" -maxdepth 6 -type f -print >&2 || true
    exit 1
  fi
  grep -Fq "name: $PLUGIN_NAME" "$skill_file"
  grep -Fq "version: \"$expected\"" "$skill_file"
  printf 'OK: installed canonical skill is %s at %s\n' "$expected" "$skill_file"
}

write_marketplace "$OLD_VERSION" "$OLD_REF" "$OLD_SHA"

copilot plugin marketplace add "$MARKETPLACE_ROOT"
copilot plugin marketplace browse "$MARKETPLACE_NAME" 2>&1 | tee "$SANDBOX/marketplace-old.txt"
grep -Fq "$PLUGIN_NAME" "$SANDBOX/marketplace-old.txt"

copilot plugin install "$PLUGIN_NAME@$MARKETPLACE_NAME"
assert_installed_version "$OLD_VERSION"
assert_installed_skill "$OLD_VERSION"

write_marketplace "$NEW_VERSION" "$NEW_REF" "$NEW_SHA"
copilot plugin marketplace update "$MARKETPLACE_NAME"
copilot plugin marketplace browse "$MARKETPLACE_NAME" 2>&1 | tee "$SANDBOX/marketplace-new.txt"
grep -Fq "$PLUGIN_NAME" "$SANDBOX/marketplace-new.txt"

# This is the lifecycle property under test. Do not replace it with uninstall + install.
copilot plugin update "$PLUGIN_NAME@$MARKETPLACE_NAME"
assert_installed_version "$NEW_VERSION"
assert_installed_skill "$NEW_VERSION"

copilot plugin uninstall "$PLUGIN_NAME@$MARKETPLACE_NAME"
if copilot plugin list 2>&1 | tee "$SANDBOX/plugins-after-uninstall.txt" | grep -Fq "$PLUGIN_NAME@$MARKETPLACE_NAME"; then
  echo "ERROR: plugin remains installed after native uninstall" >&2
  exit 1
fi

copilot plugin marketplace remove "$MARKETPLACE_NAME"

echo "OK: Copilot native lifecycle verified $OLD_REF@$OLD_SHA -> $NEW_REF@$NEW_SHA -> uninstall"
