#!/usr/bin/env python3
"""Inline agents/_common.md into agents, write Claude Code agents (.claude/agents) and Claude skills (skills/<name>/SKILL.md)."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
common = (root / "agents/_common.md").read_text(encoding="utf-8").strip()
(root / ".claude/agents").mkdir(parents=True, exist_ok=True)
for f in sorted((root / "agents").glob("*.md")):
    if f.name.startswith("_"): continue
    text = f.read_text(encoding="utf-8").replace("{{COMMON}}", common)
    (root / ".claude/agents" / f.name).write_text(text, encoding="utf-8")
    name = f.stem
    skill = re.sub(r"^(tools|model):.*\n", "", text, flags=re.M)
    d = root / "skills" / name; d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(skill, encoding="utf-8")
    print("built", name)
