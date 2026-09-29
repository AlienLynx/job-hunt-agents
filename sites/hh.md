# hh.ru and rabota.by (same platform, same page structure)

Status: **tested** (rabota.by, September 2026, read-only, built-in browser with a logged-in session). hh.ru uses the same structure, not separately tested.

Base: `https://rabota.by` or `https://hh.ru`.

| Need | URL | Notes |
|---|---|---|
| Applications and invitations | `/applicant/negotiations` | Paged with `?page=N`, zero-based (`page=1` is the second page). 10 to 20 items per page. Tabs show counts: interview, waiting, rejected, deleted. |
| Profile and resume list | `/applicant/profile/me` | Shows "applied N times" (all-time, larger than the visible list), all resumes with titles, search settings, contacts, work history. `/applicant/resumes` redirects here. |
| Vacancy search | `/search/vacancy?text=<kw>&area=<id>&schedule=remote&order_by=publication_time` | Filters go in the URL. Belarus area id is 16 (verify on first run from the area filter). Results are cards readable as text. |
| Vacancy page | `/vacancy/<id>` | Read requirements once. |

Status labels on the applications list (Russian): `Собеседование` interview, `Приглашение` invitation, `Отказ` rejected, `Просмотрен` viewed, `Не просмотрен` not viewed, `Выход на работу` offer.

Known gaps:
- The list does not show which resume was used. Open each application's chat: the resume is visible there. Only do this for rows without a stored resume.
- Page text may need a 2 to 3 second wait after navigation before it is readable.
- Do not click "Откликнуться", "Отказаться" or "Поднять в поиске". Read-only.
