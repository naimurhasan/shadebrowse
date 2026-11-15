#!/bin/bash
set -euo pipefail
BROWSER="${BROWSER:-$HOME/src/out/Release/chrome}"
PAGE="file://$(cd "$(dirname "$0")" && pwd)/fingerprint.html"

run() {
  local label="$1"
  shift
  local profile
  profile="$(mktemp -d)"
  local json
  json="$("$BROWSER" --headless=new --no-first-run --user-data-dir="$profile" \
    --timeout=8000 --dump-dom "$@" "$PAGE" 2>/dev/null |
    sed -n "/<pre id=\"out\">/,/<\/pre>/p" | sed "s/<[^>]*>//g")"
  rm -rf "$profile"
  echo "== $label"
  echo "$json"
}

run "stock (shade off)" --shade-seed=off
run "seed 42 (run 1)" --shade-seed=42
run "seed 42 (run 2)" --shade-seed=42
run "seed 7" --shade-seed=7
run "deterministic seed 42 (run 1)" --shade-seed=42 --shade-deterministic
run "deterministic seed 42 (run 2)" --shade-seed=42 --shade-deterministic
