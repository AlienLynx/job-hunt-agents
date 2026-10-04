# getmatch

Status: **partly tested 2026-10-05, public list only, read-only**. Base: `https://getmatch.ru`.

| Need | URL | Notes |
|---|---|---|
| Vacancy list | `/vacancies` | Shows `Найдено N вакансий` (913 unfiltered). The `?q=` parameter is dropped by a redirect, so keyword search by URL does NOT work. Read the list and filter titles yourself, or set filters in the UI (the filter parameters are not verified). |
| Vacancy page | `/vacancies/<id>-<slug>` | Salary is shown up front. |

Notes: many roles are Russia or relocation oriented; check location and citizenship text before scoring high. Applications page: not tested.

Same read-only rules as `sites/hh.md`. Never click apply, decline, send or delete. Log in only by the user. Never solve captchas or bypass bot checks.
