#!/usr/bin/env python3
"""Check a tailored resume: LinkedIn present, every number appears in master_facts, banned filler absent."""
import re, sys, argparse

BANNED = ["passionate", "results-driven", "dynamic", "synergy", "leverage", "cutting-edge",
          "spearheaded", "seamless", "robust", "delve", "воодушевлён", "динамичн"]

def read(p):
    try: return open(p, encoding="utf-8").read()
    except Exception: return ""

def cfg_value(cfg, key):
    m = re.search(rf"^\s*{key}:\s*\"?([^\"\n#]+?)\"?\s*(#.*)?$", cfg, re.M)
    return m.group(1).strip() if m else ""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("resume"); ap.add_argument("--config", default="config.local.yaml")
    a = ap.parse_args()
    cfg = read(a.config); text = read(a.resume)
    facts = read(cfg_value(cfg, "master_facts") or "")
    problems = []
    li = cfg_value(cfg, "linkedin")
    if "require_linkedin: true" in cfg.replace('"', "") and (not li or li.lower() not in text.lower()):
        problems.append(f"LinkedIn link missing ({li or 'not set in config'})")
    if facts:
        for n in sorted(set(re.findall(r"\d[\d.,]*\s?%?", text))):
            n = n.strip()
            if len(n) >= 2 and n not in facts and not re.fullmatch(r"(19|20)\d\d", n):
                problems.append(f"number not found in master_facts: {n}")
    else:
        problems.append("master_facts not readable, numbers not verified")
    low = text.lower()
    for w in BANNED:
        if w in low: problems.append(f"filler word: {w}")
    if "—" in text or "–" in text: problems.append("long dash found, use commas")
    print("OK" if not problems else "\n".join(problems))
    sys.exit(1 if problems else 0)

if __name__ == "__main__": main()
