#!/usr/bin/env python3
"""Optional hh.ru / rabota.by API reader (applicant side, read-only). No dependencies, no tokens spent.

STATUS: UNTESTED against the live API (no token was available when written). Verify on first use.
Docs: https://github.com/hhru/api  (register an app at https://dev.hh.ru)

Why: the web UI does not show which resume an application used; the API does (`resume` in each negotiation).

Setup (once, you do this yourself; never paste secrets into chat):
  export HH_CLIENT_ID=...  HH_CLIENT_SECRET=...  HH_REDIRECT_URI=...   # from dev.hh.ru
  python3 scripts/hh_api.py auth-url                  # open the printed URL, log in, allow
  python3 scripts/hh_api.py token --code <code from the redirect URL>  # saves the token to a local file
Or set HH_TOKEN yourself and skip the above.

Use:
  python3 scripts/hh_api.py resumes                     -> JSON list of your resumes
  python3 scripts/hh_api.py negotiations --out stats-rows.json   -> application rows with the resume title
Add --host rabota.by for the Belarus site (default hh.ru). Read-only: only GET requests are sent.
"""
import argparse, json, os, pathlib, sys, urllib.parse, urllib.request, urllib.error

API = "https://api.hh.ru"
TOKEN_FILE = pathlib.Path(os.environ.get("HH_TOKEN_FILE", "~/.jobhunt/hh_token.json")).expanduser()
UA = "job-hunt-agents/0.1 (personal use)"
STATUS = {"response": "viewed", "invitation": "invited", "interview": "interview",
          "discard": "rejected", "hired": "offer", "offer": "offer"}


def token():
    t = os.environ.get("HH_TOKEN")
    if t:
        return t
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text())["access_token"]
    sys.exit("No token. Set HH_TOKEN or run: hh_api.py auth-url, then hh_api.py token --code ...")


def get(path, host, params=None):
    p = dict(params or {}); p["host"] = host
    req = urllib.request.Request(f"{API}{path}?{urllib.parse.urlencode(p)}",
                                 headers={"Authorization": f"Bearer {token()}", "HH-User-Agent": UA, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} on GET {path}: {e.read().decode()[:300]}")


def cmd_auth_url(a):
    cid = os.environ.get("HH_CLIENT_ID") or sys.exit("Set HH_CLIENT_ID")
    q = {"response_type": "code", "client_id": cid}
    if os.environ.get("HH_REDIRECT_URI"):
        q["redirect_uri"] = os.environ["HH_REDIRECT_URI"]
    base = "https://rabota.by" if a.host == "rabota.by" else "https://hh.ru"
    print(f"{base}/oauth/authorize?{urllib.parse.urlencode(q)}")


def cmd_token(a):
    data = {"grant_type": "authorization_code", "code": a.code,
            "client_id": os.environ.get("HH_CLIENT_ID", ""), "client_secret": os.environ.get("HH_CLIENT_SECRET", "")}
    if os.environ.get("HH_REDIRECT_URI"):
        data["redirect_uri"] = os.environ["HH_REDIRECT_URI"]
    req = urllib.request.Request(f"{API}/token", data=urllib.parse.urlencode(data).encode(),
                                 headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            tok = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:300]}")
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(tok))
    print(f"Token saved to {TOKEN_FILE} (keep it private; it is outside the repo).")


def cmd_resumes(a):
    d = get("/resumes/mine", a.host)
    out = [{"id": r.get("id"), "title": r.get("title"), "updated": r.get("updated_at"),
            "views": (r.get("views_count") or r.get("total_views")), "new_views": r.get("new_views")}
           for r in d.get("items", [])]
    print(json.dumps(out, ensure_ascii=False, indent=1))


def cmd_negotiations(a):
    rows, page = [], 0
    while True:
        d = get("/negotiations", a.host, {"page": page, "per_page": 100, "status": "all"})
        items = d.get("items", [])
        for n in items:
            v, e = n.get("vacancy") or {}, (n.get("vacancy") or {}).get("employer") or {}
            state = (n.get("state") or {}).get("id", "")
            st = STATUS.get(state, "viewed")
            if state == "response" and not n.get("viewed_by_opponent", True):
                st = "not_viewed"
            rows.append({"id": f"{'hh' if a.host == 'hh.ru' else 'rabota_by'}:{n.get('id')}",
                         "site": "hh" if a.host == "hh.ru" else "rabota_by",
                         "company": e.get("name", ""), "role": v.get("name", ""),
                         "date": (n.get("created_at") or "")[:10], "status": st,
                         "resume": (n.get("resume") or {}).get("title", ""), "note": "from API", "why": ""})
        page += 1
        if page >= d.get("pages", 1) or not items:
            break
    s = json.dumps(rows, ensure_ascii=False, indent=1)
    if a.out:
        pathlib.Path(a.out).write_text(s, encoding="utf-8"); print(f"{len(rows)} rows -> {a.out}")
    else:
        print(s)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="hh.ru", choices=["hh.ru", "rabota.by"])
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("auth-url").set_defaults(f=cmd_auth_url)
    t = sp.add_parser("token"); t.add_argument("--code", required=True); t.set_defaults(f=cmd_token)
    sp.add_parser("resumes").set_defaults(f=cmd_resumes)
    n = sp.add_parser("negotiations"); n.add_argument("--out"); n.set_defaults(f=cmd_negotiations)
    a = ap.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
