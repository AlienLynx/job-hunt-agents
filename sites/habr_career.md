# Habr Career

Status: **tested 2026-10-05, public search only, read-only** (no log-in tried). Base: `https://career.habr.com`.

| Need | URL | Notes |
|---|---|---|
| Vacancy search | `/vacancies?q=<text>&type=all` | Page text shows `Найдена N вакансия`. 50 vacancy links per page; cards are `.vacancy-card` (date, company, title, salary or "Зарплата не указана", city, skills). Other filter parameters (remote, salary, qualification) are not verified. |
| Vacancy page | `/vacancies/<id>` | The "Откликнуться" link on cards is `#guest-response`: do not click. |

Notes: IT-heavy, many Russia-based roles. Applications and resumes pages: not tested.

Same read-only rules as `sites/hh.md`. Never click apply, decline, send or delete. Log in only by the user. Never solve captchas or bypass bot checks.
