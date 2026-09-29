#!/usr/bin/env bash
# Builds one .skill file per agent for the Claude app (Settings > Skills > upload). Output: dist/*.skill
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; python3 "$ROOT/scripts/build.py"
TMP="$(mktemp -d)"; mkdir -p "$ROOT/dist"
for d in "$ROOT"/skills/*/; do n=$(basename "$d"); (cd "$ROOT/skills" && zip -qr "$TMP/$n.skill" "$n"); cp "$TMP/$n.skill" "$ROOT/dist/$n.skill"; echo "dist/$n.skill"; done
rm -rf "$TMP"
