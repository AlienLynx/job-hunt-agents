# job-hunt-agents

[Русская версия](README.ru.md)

Three small agents for Claude and Claude Code that run your job search: track what happened to your applications, find vacancies that fit, and tailor resumes without inventing facts.

| Agent | What it does |
|---|---|
| `stats-collector` | Reads your applications and chats on job sites: which resume went where, invitations, rejections, silence. Writes compact `stats.json` for agents and a readable `report.html` for you. Guesses why applications failed and lists problems in your profile. |
| `vacancy-scout` | Searches by your filters (locations, keywords, remote, salary), scores each vacancy against each of your resumes in percent, and says "send resume X" or "tailor: change Y". |
| `resume-tailor` | Rebuilds a resume for one vacancy using only facts you confirmed. Asks about anything unverified, keeps your LinkedIn link in every resume, checks numbers, builds md and PDF. |

Design goals: read-only on job sites (no auto-apply), minimal tokens (page text instead of screenshots, deterministic scripts for scoring and reports, skip what is already stored), no personal data in the repo.

## Site support

| Site | Status |
|---|---|
| hh.ru, rabota.by | Tested (rabota.by, read-only). See `sites/hh.md`. |
| Hirify | Tested through its MCP connector. See `sites/hirify.md`. |
| praca.by, Jooble, Habr Career, getmatch, superjob.ru, rabota.ru | Untested. The agent discovers the pages on first run and records them. See `sites/`. |
| LinkedIn | Experimental, off by default. Mind the site's terms. |

Pull requests with verified adapters are welcome.

## Install

**Claude Code**

```bash
git clone <this repo> && cd job-hunt-agents
scripts/install.sh            # copies agents to ~/.claude/agents
cp config.example.yaml config.local.yaml   # or let the agent ask you
claude --chrome               # browser access for logged-in sites
```

Or as a plugin: `/plugin marketplace add AlienLynx/job-hunt-agents`, then `/plugin install job-hunt-agents@job-hunt-agents`.

**First run: guided setup**

```bash
python3 scripts/setup.py      # asks about profile, sites, search filters; writes config.local.yaml
```

Or say "use job-hunt-setup". It interviews you in chat, checks that a browser tool and Hirify are connected, checks you are logged in to each site, reads your resumes and builds `master-facts.md` from facts you confirm. Then: "use stats-collector", "use vacancy-scout", "use resume-tailor for <vacancy link>".

**Claude app (Cowork / desktop)**

```bash
scripts/pack_skills.sh        # creates dist/*.skill
```

Upload each `.skill` in Settings, Skills. The built-in browser pane is used for sites.

## Which resume was used (hh.ru, rabota.by)

The web UI no longer shows it. Order the stats agent tries: (1) optional hh API, `scripts/hh_api.py` (needs a token from dev.hh.ru, untested against the live API, read-only); (2) inference from the "who viewed your resume" page, marked "likely"; (3) leave empty, fill by hand. No token needed for 2 and 3.

## Secrets and tests

Optional API tokens go in `.env` (copy `.env.example`, gitignored) or `~/.jobhunt/.env`. Only the scripts read it; agents never read or print it and never type passwords into sites. Prefer tokens over passwords, and do not store site passwords on disk unless you accept plain text.

Tests: `python3 -m unittest discover -s tests -v` (also run by GitHub Actions on every push).

## Cost

All agents run on the cheapest model (`model: haiku`). Scoring, merging and reports are Python scripts, so the model only reads pages and classifies. You can raise the model for `resume-tailor` in `agents/resume-tailor.md` if wording quality matters more than cost, then run `python3 scripts/build.py`.

## Other harnesses (Codex, DeepSeek Harness, others)

Not tested. The prompts in `agents/*.md` are plain markdown and the scripts are plain Python, so they carry over. See `AGENTS.md`: read the agent file plus `agents/_common.md` and follow it. Two things to adapt:

- Browser: the prompts name Claude's browser tools. Connect a browser MCP server (for example Playwright MCP) and swap the tool names. DeepSeek Harness can use MCP servers as a tool source, but MCP is not enabled by default there.
- The `model:` line in the frontmatter is Claude-specific and ignored elsewhere.

`python3 scripts/setup.py` works in any terminal.

## Configuration

Everything is a variable in `config.local.yaml` (see `config.example.yaml`): profile, LinkedIn, paths, enabled sites, locations, keywords, exclusions, remote mode, salary, match threshold, rules. Edit the file, or tell Claude "set locations to Minsk and Remote" and it edits the file. If no file exists the agent asks once and creates it, or keeps values in the chat only if you say so.

Data (stats, vacancies, tailored resumes) is written to `paths.data_dir`. `config.local.yaml` and the data folder are gitignored.

## Login

Agents never type passwords. If a site is not logged in, the agent stops and asks you to log in in the browser, then continues when you reply "done". If no browser tool is connected, the agent stops and tells you how to connect one.

- Claude app: the built-in browser pane.
- Claude Code: Claude in Chrome (https://code.claude.com/docs/en/chrome). Not every setup has it, so the agent checks first and never falls back to scraping.

## Files

```
agents/            source prompts (edit here), _common.md is inlined into each
.claude/agents/    generated for Claude Code
skills/            generated for the Claude app
sites/             per-site notes: URLs, statuses, known gaps
scripts/           setup.py, render_report.py, match.py, check_resume.py, build_pdf.py, build.py
examples/          stats.example.json
```

After editing `agents/*.md`, run `python3 scripts/build.py`.

## Limits

Sites change their pages, so adapters can break. Match percentages are a keyword pre-score refined by the model, a ranking aid and not a verdict. Statistics only cover applications visible on the site. Failure reasons are hypotheses. Use it within each site's terms, read-only, at a human pace.

License: MIT.
