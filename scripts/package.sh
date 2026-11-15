#!/bin/bash
set -euo pipefail
SRC="${SRC:-$HOME/chromium/src}"
VERSION="$(cut -d= -f2 "$SRC/chrome/VERSION" | paste -sd.)"
NAME="shadebrowse-$VERSION-linux-x64"
OUT="${OUT:-$PWD}/$NAME"

rm -rf "$OUT" && mkdir -p "$OUT"
cd "$SRC/out/Release"
cp -r chrome chrome_sandbox chromedriver chrome_crashpad_handler locales "$OUT"/
cp ./*.pak ./*.bin ./*.dat ./*.so ./*.so.* ./*.json "$OUT"/ 2>/dev/null || true
tar -C "$(dirname "$OUT")" -cJf "$OUT.tar.xz" "$NAME"
echo "$OUT.tar.xz"
