## Step 0: setup (do this first, every run, briefly)
1. Find config: `$JOBHUNT_CONFIG`, else `./config.local.yaml`, else `~/.jobhunt/config.yaml`. Read it as text. If none exists, ask the user ONCE for: name, LinkedIn URL, data_dir, sites, locations, keywords. Write the answers to `config.local.yaml` (or keep them in chat if the user says so, and say they will not persist). Later edits: the user says "set X to Y", you edit the file.
2. Check for a browser tool. Claude app: the built-in browser (`mcp__Claude_Browser__*`) or Claude in Chrome. Claude Code: Claude in Chrome (`claude --chrome`, docs: https://code.claude.com/docs/en/chrome). Deferred tools: load them with one ToolSearch call. If no browser tool exists, STOP and tell the user exactly how to connect one. Do not fall back to curl or scraping.
3. Open the site. If not logged in, ask the user to log in themselves in that browser and reply "done". Never type passwords, codes or tokens. Never solve captchas.
4. Read `sites/<site>.md` for URLs and selectors of that site. If a site is marked untested, discover the URLs on the first run and note what worked in `<data_dir>/site-notes.md`.

## Rules for every run
- Read-only on job sites: never apply, send messages, delete, archive or edit a profile. Never click buttons inside applications lists or chats. Open pages by URL and read text only.
- Secrets: never read, print or copy `.env` files, tokens or passwords. Only scripts read them. Never type passwords into sites.
- Cheapest model: do all page reading and classification on the cheapest available model. Use scripts for scoring, merging and reports. Do not delegate to a pricier model.
- Token thrift: use page text (`get_page_text`/`read_page`), not screenshots. Skip items already stored (by id). Stop at `max_vacancies_per_run`. Write compact JSON. Keep reasoning short: classify, do not essay.
- Everything you write goes to `data_dir`. Never write personal data anywhere else.
- If something cannot be verified, say so in one line. Do not invent.
