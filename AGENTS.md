# AGENTS.md

Job-search agents, usable from any agent harness (Codex, DeepSeek Harness, Claude Code, others).
The prompts are plain markdown. Claude-specific files are generated from them.

## Agents

| Name | Prompt file | Use for |
|---|---|---|
| job-hunt-setup | `agents/job-hunt-setup.md` | First run: config, browser and log-in check, master facts |
| stats-collector | `agents/stats-collector.md` | Application statistics and report |
| vacancy-scout | `agents/vacancy-scout.md` | Find and score vacancies |
| resume-tailor | `agents/resume-tailor.md` | Tailor a resume to one vacancy |

To run one: read `agents/<name>.md`, then read `agents/_common.md` (it replaces `{{COMMON}}`), then follow it as your instructions.

## Rules for every agent

- Read-only on job sites. Never apply, decline, send, delete or edit.
- Never type passwords, codes or tokens. If a site needs log-in, ask the user to log in and reply "done".
- Use the cheapest available model for all agentic work; scripts do scoring, merging and reports.
- Never invent resume facts. Only `master_facts` counts.
- Write personal data only to `config.local.yaml` and the `data_dir` folder (both gitignored).

## Tools the prompts assume

- A browser that can read page text: a browser MCP server (for example Playwright MCP). In Claude: built-in browser or Claude in Chrome. In other harnesses, replace the Claude tool names in the prompts with your browser tool.
- A shell and Python 3 for `scripts/*.py`. These scripts need no harness.
- Optional: Hirify MCP connector (see `sites/hirify.md`).

## Setup without an agent

```bash
python3 scripts/setup.py
```
