# superjob.ru

Status: **untested**. No URLs are verified. On the first run the agent must:
1. Open `https://www.superjob.ru`, confirm the user is logged in (ask them to log in if not).
2. Find the pages for: my applications (responses), my resumes, and vacancy search with filters in the URL.
3. Write what worked (URLs, status wording, paging, whether the resume used is visible) to `<data_dir>/site-notes.md`, then copy the working parts here via a pull request.

Optional: SuperJob has an official API (https://api.superjob.ru, needs an app key from the user's own account). Not wired up here.

Same read-only rules as `sites/hh.md`. Never click apply, decline, send or delete. Log in only by the user.
