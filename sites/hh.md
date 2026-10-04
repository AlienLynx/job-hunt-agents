# hh.ru and rabota.by (same platform, same page structure)

Status: **tested** (rabota.by, September 2026, read-only, built-in browser with a logged-in session). hh.ru uses the same structure, not separately tested.

Base: `https://rabota.by` or `https://hh.ru`.

| Need | URL | Notes |
|---|---|---|
| Applications and invitations | `/applicant/negotiations` | Paged with `?page=N`, zero-based (`page=1` is the second page). 10 to 20 items per page. Tabs show counts: interview, waiting, rejected, deleted. |
| Profile and resume list | `/applicant/profile/me` | Shows "applied N times" (all-time, larger than the visible list), all resumes with titles, search settings, contacts, work history. `/applicant/resumes` redirects here. |
| Resume list with weekly stats | `/applicant/my_resumes` | Per resume: weekly shows, views, invitations. Links to each resume's views log. |
| Who viewed a resume | `/applicant/resumeview/history?resumeHash=<hash>` | Company and date of every view, all time (also counts a company's repeat views). Hashes come from `/applicant/my_resumes`. `/applicant/resumeview_history` is a 404. |
| Vacancy search | `/search/vacancy?text=<kw>&area=<id>&schedule=remote&order_by=publication_time` | Filters go in the URL. Belarus area id is 16 (verify on first run from the area filter). Results are cards readable as text. |
| Vacancy page | `/vacancy/<id>` | Read requirements once. |

Status labels on the applications list (Russian): `Собеседование` interview, `Приглашение` invitation, `Отказ` rejected, `Просмотрен` viewed, `Не просмотрен` not viewed, `Выход на работу` offer.

Known gaps:
- On rabota.by the chat and the vacancy page no longer show which resume an application used (checked 2026-10). Infer it from the views log: if exactly one resume was opened by that company, mark it "likely". The list date is the last activity, not the application date.
- Page text may need a 2 to 3 second wait after navigation before it is readable.
- Do not click "Откликнуться", "Отказаться" or "Поднять в поиске". Read-only.
