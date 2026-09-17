#!/usr/bin/env bash
set -euo pipefail

PLUGIN_NAME="github-build-or-reuse"
MARKETPLACE_NAME="github-build-or-reuse-lifecycle"
REPOSITORY="ghspain/github-build-or-reuse"
REPOSITORY_URL="https://github.com/$REPOSITORY.git"
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
HTTP_SERVER_PID=""
cleanup() {
  if [[ -n "$HTTP_SERVER_PID" ]]; then
    kill "$HTTP_SERVER_PID" 2>/dev/null || true
    wait "$HTTP_SERVER_PID" 2>/dev/null || true
  fi
  rm -rf "$SANDBOX"
}
trap cleanup EXIT

TEST_HOME="$SANDBOX/home"
MARKETPLACE_WORK="$SANDBOX/marketplace-work"
MARKETPLACE_BARE="$SANDBOX/marketplace.git"
mkdir -p "$TEST_HOME" "$SANDBOX/copilot-home" "$SANDBOX/cache" "$MARKETPLACE_WORK"

export HOME="$TEST_HOME"
export COPILOT_HOME="$SANDBOX/copilot-home"
export COPILOT_CACHE_HOME="$SANDBOX/cache"
export XDG_CACHE_HOME="$SANDBOX/cache"
export COPILOT_AUTO_UPDATE="false"

resolve_release_commit() {
  local ref="$1"
  local direct dereferenced
  direct="$(git ls-remote "$REPOSITORY_URL" "refs/tags/$ref" | awk 'NR==1 {print $1}')"
  dereferenced="$(git ls-remote "$REPOSITORY_URL" "refs/tags/$ref^{}" | awk 'NR==1 {print $1}')"
  if [[ -n "$dereferenced" ]]; then
    printf '%s\n' "$dereferenced"
  else
    printf '%s\n' "$direct"
  fi
}

assert_release_commit() {
  local ref="$1"
  local expected="$2"
  local actual
  actual="$(resolve_release_commit "$ref")"
  if [[ "$actual" != "$expected" ]]; then
    echo "ERROR: $ref resolves to $actual, expected immutable commit $expected" >&2
    exit 1
  fi
  echo "OK: $ref resolves to expected commit $expected"
}

write_marketplace() {
  local version="$1"
  local ref="$2"
  local sha="$3"
  cat > "$MARKETPLACE_WORK/marketplace.json" <<JSON
{
  "name": "$MARKETPLACE_NAME",
  "owner": {
    "name": "GitHub Community Spain"
  },
  "metadata": {
    "description": "Ephemeral Git marketplace used only for lifecycle verification"
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
        "sha": "$sha",
        "path": "."
      }
    }
  ]
}
JSON
}

publish_marketplace_state() {
  local version="$1"
  local ref="$2"
  local sha="$3"
  write_marketplace "$version" "$ref" "$sha"
  git -C "$MARKETPLACE_WORK" add marketplace.json
  git -C "$MARKETPLACE_WORK" commit -m "marketplace: publish $version" >/dev/null
  git -C "$MARKETPLACE_WORK" push origin main >/dev/null
  # Enable read-only dumb HTTP cloning from the local bare repository.
  git --git-dir="$MARKETPLACE_BARE" update-server-info
}

dump_state() {
  echo "--- Copilot lifecycle diagnostic state ---" >&2
  echo "COPILOT_HOME=$COPILOT_HOME" >&2
  echo "COPILOT_CACHE_HOME=$COPILOT_CACHE_HOME" >&2
  copilot plugin marketplace list --json >&2 || true
  copilot plugin list --json >&2 || true
  find "$COPILOT_HOME" -maxdepth 7 -type f -print >&2 || true
  if [[ -f "$COPILOT_HOME/config.json" ]]; then
    cat "$COPILOT_HOME/config.json" >&2 || true
  fi
  echo "--- Copilot process logs ---" >&2
  for logfile in "$COPILOT_HOME"/logs/process-*.log; do
    if [[ -f "$logfile" ]]; then
      echo "### $logfile" >&2
      tail -n 160 "$logfile" >&2 || true
    fi
  done
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

assert_release_commit "$OLD_REF" "$OLD_SHA"
assert_release_commit "$NEW_REF" "$NEW_SHA"

# Create a genuinely remote Git marketplace fixture that can advance while
# keeping the same registered marketplace identity. It is served read-only over
# HTTP from localhost; the plugin payload itself is fetched from the two real,
# SHA-verified GitHub releases above.
git init --bare "$MARKETPLACE_BARE" >/dev/null
git -C "$MARKETPLACE_WORK" init >/dev/null
git -C "$MARKETPLACE_WORK" config user.name "Lifecycle Test"
git -C "$MARKETPLACE_WORK" config user.email "lifecycle@example.invalid"
git -C "$MARKETPLACE_WORK" remote add origin "$MARKETPLACE_BARE"
git -C "$MARKETPLACE_WORK" checkout -b main >/dev/null
publish_marketplace_state "$OLD_VERSION" "$OLD_REF" "$OLD_SHA"
git --git-dir="$MARKETPLACE_BARE" symbolic-ref HEAD refs/heads/main
git --git-dir="$MARKETPLACE_BARE" update-server-info

auto_port="$(python - <<'PY'
import socket
with socket.socket() as s:
    s.bind(('127.0.0.1', 0))
    print(s.getsockname()[1])
PY
)"
python -m http.server "$auto_port" --bind 127.0.0.1 --directory "$SANDBOX" >"$SANDBOX/http.log" 2>&1 &
HTTP_SERVER_PID=$!
sleep 1
MARKETPLACE_URL="http://127.0.0.1:$auto_port/marketplace.git"
git ls-remote "$MARKETPLACE_URL" refs/heads/main >/dev/null

copilot plugin marketplace add "$MARKETPLACE_URL"
copilot plugin marketplace browse "$MARKETPLACE_NAME" --json | tee "$SANDBOX/marketplace-old.json"
copilot plugin install "$PLUGIN_NAME@$MARKETPLACE_NAME"
assert_installed_version "$OLD_VERSION"
assert_installed_skill "$OLD_VERSION"

publish_marketplace_state "$NEW_VERSION" "$NEW_REF" "$NEW_SHA"
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
