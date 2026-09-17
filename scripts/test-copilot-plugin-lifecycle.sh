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
mkdir -p "$MARKETPLACE_ROOT" "$TEST_HOME" "$SANDBOX/copilot-home" "$SANDBOX/cache"

export HOME="$TEST_HOME"
export COPILOT_HOME="$SANDBOX/copilot-home"
export COPILOT_CACHE_HOME="$SANDBOX/cache"
export XDG_CACHE_HOME="$SANDBOX/cache"
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

dump_state() {
  echo "--- Copilot lifecycle diagnostic state ---" >&2
  echo "COPILOT_HOME=$COPILOT_HOME" >&2
  echo "COPILOT_CACHE_HOME=$COPILOT_CACHE_HOME" >&2
  copilot plugin marketplace list --json >&2 || true
  copilot plugin list --json >&2 || true
  find "$COPILOT_HOME" -maxdepth 6 -type f -print >&2 || true
  if [[ -f "$COPILOT_HOME/config.json" ]]; then
    cat "$COPILOT_HOME/config.json" >&2 || true
  fi
  echo "--- end diagnostic state ---" >&2
}

assert_installed_version() {
  local expected="$1"
  local output="$SANDBOX/plugins-$expected.json"
  copilot plugin list --json | tee "$output"
  if ! python - "$output" "$PLUGIN_NAME" "$MARKETPLACE_NAME" "$expected" <<'PY'
import json
import pathlib
import sys

path, name, marketplace, version = sys.argv[1:]
rows = json.loads(pathlib.Path(path).read_text())
matching = [
    row for row in rows
    if row.get("name") == name and row.get("marketplace") == marketplace
]
if len(matching) != 1:
    raise SystemExit(f"expected one installed row for {name}@{marketplace}, got {matching!r}")
row = matching[0]
if row.get("version") != version:
    raise SystemExit(f"expected version {version}, got {row.get('version')!r}")
if row.get("enabled") is not True:
    raise SystemExit(f"expected enabled plugin, got {row!r}")
PY
  then
    dump_state
    exit 1
  fi
}

assert_installed_skill() {
  local expected="$1"
  local skill_file
  skill_file="$(find "$COPILOT_HOME" -type f -path "*/skills/$PLUGIN_NAME/SKILL.md" -print -quit)"
  if [[ -z "$skill_file" ]]; then
    echo "ERROR: installed canonical SKILL.md was not found below $COPILOT_HOME" >&2
    dump_state
    exit 1
  fi
  grep -Fq "name: $PLUGIN_NAME" "$skill_file"
  grep -Fq "version: \"$expected\"" "$skill_file"
  printf 'OK: installed canonical skill is %s at %s\n' "$expected" "$skill_file"
}

write_marketplace "$OLD_VERSION" "$OLD_REF" "$OLD_SHA"

copilot plugin marketplace add "$MARKETPLACE_ROOT"
copilot plugin marketplace browse "$MARKETPLACE_NAME" --json | tee "$SANDBOX/marketplace-old.json"

copilot plugin install "$PLUGIN_NAME@$MARKETPLACE_NAME"
assert_installed_version "$OLD_VERSION"
assert_installed_skill "$OLD_VERSION"

write_marketplace "$NEW_VERSION" "$NEW_REF" "$NEW_SHA"
copilot plugin marketplace update "$MARKETPLACE_NAME"
copilot plugin marketplace browse "$MARKETPLACE_NAME" --json | tee "$SANDBOX/marketplace-new.json"

# This is the lifecycle property under test. Do not replace it with uninstall + install.
copilot plugin update "$PLUGIN_NAME@$MARKETPLACE_NAME"
assert_installed_version "$NEW_VERSION"
assert_installed_skill "$NEW_VERSION"

copilot plugin uninstall "$PLUGIN_NAME@$MARKETPLACE_NAME"
if copilot plugin list --json | python -c 'import json,sys; rows=json.load(sys.stdin); raise SystemExit(any(r.get("name") == "github-build-or-reuse" and r.get("marketplace") == "github-build-or-reuse-lifecycle" for r in rows))'; then
  :
else
  echo "ERROR: plugin remains installed after native uninstall" >&2
  dump_state
  exit 1
fi

copilot plugin marketplace remove "$MARKETPLACE_NAME"

echo "OK: Copilot native lifecycle verified $OLD_REF@$OLD_SHA -> $NEW_REF@$NEW_SHA -> uninstall"
