# Hirify

Status: **tested through its MCP connector** (not a browser site). If the user has a Hirify account with agent access, use the `hirify_*` tools instead of the browser: search with filters (`countries`, `regions`, `grade`, `skills`, `work_format`, `salary_from`, `period`), read a vacancy by slug (counts against a daily quota, so read only shortlisted ones), list feeds and profiles.

Tested 2026-10-05: `hirify_search_vacancies` with `{"search": "product manager", "work_format": "remote"}` returned 1677 vacancies. Use the `search` parameter for title queries (see `filters.guide` via `hirify_invoke_capability`). `{"countries": ["BY"]}` and `{"countries": ["BY"], "grade": ["lead"]}` returned 0, so do not rely on `countries`. Cards include `has_applied` and `in_tracker`, so skip those.

Applications: `applications.list` (capability) returns the user's applications, both sent through Hirify and logged in the tracker (title, company, date_applied, stage). `stats-collector` should use it for Hirify. It does not show a resume. The user had 26 entries (page 1 of 2 read).

Known issue: the `specializations` filter returned 0 results even for valid codes. Use `countries` or `regions` plus `grade`, then triage by title.

Hirify is software-centric, so hardware and electronics vacancies are rare there.
