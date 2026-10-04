# Jooble

Status: **blocked by a Cloudflare challenge 2026-10-05** ("Just a moment...") on `by.jooble.org/SearchResult?ukw=<text>`. Agents must not bypass bot checks. Use the official API with the user's own key (https://jooble.org/api/about, key in `.env` as `JOOBLE_API_KEY`; not wired up here) or let the user pass the check in the browser and retry.

Aggregator: the same vacancy often appears on other sites; dedupe by title plus company. Use for `vacancy-scout` only.

Same read-only rules as `sites/hh.md`. Never click apply, decline, send or delete. Log in only by the user. Never solve captchas or bypass bot checks.
