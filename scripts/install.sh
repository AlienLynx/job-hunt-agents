#!/usr/bin/env bash
# Usage: scripts/install.sh [--user|--project <path>]
# Claude Code agents -> ~/.claude/agents (user) or <project>/.claude/agents. Skills for the Claude app: run scripts/pack_skills.sh
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/scripts/build.py"
DEST="${HOME}/.claude/agents"
if [ "$1" = "--project" ] && [ -n "$2" ]; then DEST="$2/.claude/agents"; fi
mkdir -p "$DEST" && cp "$ROOT"/.claude/agents/*.md "$DEST"/
echo "Installed to $DEST. Keep this repo folder: agents read sites/*.md, scripts/*.py and config from it."
echo "Set JOBHUNT_CONFIG=/path/to/config.local.yaml or run agents from the repo folder."
echo "Next: python3 scripts/setup.py (guided config), or say: use job-hunt-setup"
