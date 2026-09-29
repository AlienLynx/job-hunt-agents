#!/usr/bin/env python3
"""Cheap keyword pre-score of vacancies against resumes. No dependencies, no tokens.
resumes.json:   [{"id": "...", "file": "...", "terms": ["..."]}]
vacancies.json: [{"id": "...", "title": "...", "requirements": ["..."]}]
"""
import json, re, sys, argparse

def norm(s): return re.sub(r"[^\w+#.]+", " ", s.lower()).strip()

def cover(req_terms, resume_terms, resume_text=""):
    rt = {norm(t) for t in resume_terms}
    hit = 0
    for r in req_terms:
        n = norm(r)
        if n in rt or any(n in x or x in n for x in rt if len(x) > 2) or (resume_text and n in resume_text):
            hit += 1
    return hit / max(len(req_terms), 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resumes", required=True); ap.add_argument("--vacancies", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    resumes = json.load(open(a.resumes, encoding="utf-8"))
    vacs = json.load(open(a.vacancies, encoding="utf-8"))
    texts = {}
    for r in resumes:
        try: texts[r["id"]] = norm(open(r["file"], encoding="utf-8").read())
        except Exception: texts[r["id"]] = ""
    out = []
    for v in vacs:
        reqs = v.get("requirements") or re.findall(r"\w[\w+#.]+", v.get("title", ""))
        scores = sorted(((round(cover(reqs, r.get("terms", []), texts.get(r["id"], "")) * 100), r["id"])
                         for r in resumes), reverse=True)
        best = scores[0] if scores else (0, None)
        out.append({**v, "match_pre": best[0], "best_resume": best[1], "all": scores[:3]})
    out.sort(key=lambda x: -x["match_pre"])
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"scored {len(out)}; top: " + ", ".join(f"{o['title'][:30]} {o['match_pre']}%" for o in out[:3]))

if __name__ == "__main__": main()
