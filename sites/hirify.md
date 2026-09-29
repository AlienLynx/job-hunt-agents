# Hirify

Status: **tested through its MCP connector** (not a browser site). If the user has a Hirify account with agent access, use the `hirify_*` tools instead of the browser: search with filters (`countries`, `regions`, `grade`, `skills`, `work_format`, `salary_from`, `period`), read a vacancy by slug (counts against a daily quota, so read only shortlisted ones), list feeds and profiles.

Known issue: the `specializations` filter returned 0 results even for valid codes. Use `countries` or `regions` plus `grade`, then triage by title.

Hirify is software-centric, so hardware and electronics vacancies are rare there.
