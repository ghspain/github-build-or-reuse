#!/usr/bin/env bash
set -euo pipefail

WAZA_VERSION="0.38.6"
WAZA_SHA256="a799587795fd462411ca7c7af5faccee7e24f08e41d152c10738d31334d1c063"
WAZA_URL="https://github.com/microsoft/waza/releases/download/v${WAZA_VERSION}/waza-linux-amd64"
DESTINATION="${1:-${RUNNER_TEMP:-/tmp}/waza}"

if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
  echo "ERROR: CI installer supports Linux x86_64 only." >&2
  exit 2
fi

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
curl --fail --location --silent --show-error --retry 3 --output "$tmp" "$WAZA_URL"
printf '%s  %s\n' "$WAZA_SHA256" "$tmp" | sha256sum --check --status || {
  echo "ERROR: Waza v${WAZA_VERSION} checksum verification failed." >&2
  exit 1
}
mkdir -p "$(dirname "$DESTINATION")"
install -m 0755 "$tmp" "$DESTINATION"
"$DESTINATION" --version
