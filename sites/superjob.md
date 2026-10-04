# superjob.ru

Status: **blocked by a captcha 2026-10-05** when opening search (`/vacancy/search/?keywords=...`). Agents must not solve captchas or bypass the check. Options: the user opens the site and solves it in the browser (then retry), or use the official API with the user's own key (https://api.superjob.ru, key in `.env` as `SUPERJOB_SECRET_KEY`; not wired up here).

Discovery steps once the page opens: find my responses, my resumes, and the filter URL parameters; record them in `<data_dir>/site-notes.md` and send them back as a pull request.

Same read-only rules as `sites/hh.md`. Never click apply, decline, send or delete. Log in only by the user. Never solve captchas or bypass bot checks.
