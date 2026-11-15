#!/bin/bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${WORK:-$HOME/chromium}"
export PATH="$WORK/depot_tools:$PATH"

[ -d "$WORK/depot_tools" ] || git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git "$WORK/depot_tools"
cd "$WORK"
[ -d src ] || fetch --nohooks --no-history chromium
cd src
git fetch --depth=1 origin "$(cat "$REPO/CHROMIUM_COMMIT")"
git checkout -f "$(cat "$REPO/CHROMIUM_COMMIT")"
gclient sync -D --force --nohooks
gclient runhooks

for patch in "$REPO"/patches/*.patch; do
  git apply --index "$patch"
done
cp "$REPO"/assets/icons/*.png chrome/app/theme/chromium/
cp "$REPO"/assets/logo.svg chrome/app/theme/chromium/product_logo.svg

mkdir -p out/Release
cp "$REPO/args.gn" out/Release/args.gn
gn gen out/Release
autoninja -C out/Release chrome chrome_sandbox chromedriver
