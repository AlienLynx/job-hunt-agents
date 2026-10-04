# praca.by

Status: **tested 2026-10-05, public search only, read-only** (no log-in tried). Base: `https://praca.by`.

| Need | URL | Notes |
|---|---|---|
| Vacancy search | `/search/vacancies/?search[query]=<text>` (URL-encode the brackets) | Page text shows `Найдено: N`. Many filters (city, remote, schedule, experience) are checkboxes; their URL parameters are not verified yet. Filter by text instead. |
| Vacancy page | `/vacancy/<id>/` | Result cards link here. Read requirements once. |

Notes: the page text is dominated by the city list. Extract cards with a script on `a[href*="/vacancy/"]` instead of reading all text (saves tokens). Small market: "project manager" returned 2 vacancies. Applications and resumes pages: not tested.

Same read-only rules as `sites/hh.md`. Never click apply, decline, send or delete. Log in only by the user. Never solve captchas or bypass bot checks.
