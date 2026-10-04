#!/usr/bin/env python3
"""Guided setup: asks a few questions, writes config.local.yaml and the data folder.

Works with any harness (plain terminal). Usage:
  python3 scripts/setup.py            interactive
  python3 scripts/setup.py --defaults write config.local.yaml from the example, no questions
Press Enter to keep the value in [brackets]. Nothing leaves your machine.
"""
import argparse, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
SITES = [
    ("hh", "hh.ru", True),
    ("rabota_by", "rabota.by", True),
    ("superjob", "superjob.ru (untested)", False),
    ("rabota_ru", "rabota.ru (untested)", False),
    ("praca_by", "praca.by (untested)", False),
    ("jooble", "Jooble aggregator (untested)", False),
    ("habr_career", "Habr Career (untested)", False),
    ("getmatch", "getmatch (untested)", False),
    ("hirify", "Hirify via MCP connector", False),
    ("linkedin", "LinkedIn (experimental, mind site terms)", False),
]
DOMAINS = {"hh": '["hh.ru"]', "rabota_by": '["rabota.by"]', "superjob": '["superjob.ru"]', "rabota_ru": '["rabota.ru"]',
           "praca_by": '["praca.by"]', "jooble": '["jooble.org"]', "habr_career": '["career.habr.com"]', "getmatch": '["getmatch.ru"]'}


def ask(prompt, default=""):
    if not sys.stdin.isatty():
        return default
    v = input(f"{prompt} [{default}]: ").strip()
    return v or default


def ask_bool(prompt, default):
    v = ask(prompt + " (y/n)", "y" if default else "n").lower()
    return v.startswith(("y", "д"))


def ask_list(prompt, default):
    v = ask(prompt + " (comma separated)", ", ".join(default))
    return [x.strip() for x in v.split(",") if x.strip()]


def q(items):
    return "[" + ", ".join('"%s"' % i.replace('"', "'") for i in items) + "]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--defaults", action="store_true")
    ap.add_argument("--out", default=str(root / "config.local.yaml"))
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    if out.exists() and not a.defaults and not ask_bool(f"{out.name} exists. Overwrite?", False):
        print("Kept the existing config. Edit it by hand or tell the agent 'set X to Y'.")
        return
    interactive = not a.defaults
    ask_ = ask if interactive else (lambda p, d="": d)
    askb = ask_bool if interactive else (lambda p, d: d)
    askl = ask_list if interactive else (lambda p, d: d)

    print("== Profile ==")
    name = ask_("Your name", "Your Name")
    linkedin = ask_("LinkedIn URL (goes into every resume)", "linkedin.com/in/your-handle")
    langs = askl("Resume languages (codes)", ["ru", "en"])
    print("== Where to keep your data (gitignored, never committed) ==")
    data = ask_("Data folder", "./jobhunt-data")
    print("== Job sites (read-only, you log in yourself) ==")
    enabled = {k: askb(f"Use {label}?", d) for k, label, d in SITES}
    hh_api = askb("Use the optional hh API to read which resume each application used? Needs a token, see scripts/hh_api.py", False)
    print("== Search ==")
    locs = askl("Locations", ["Minsk", "Belarus", "Remote"])
    kws = askl("Keywords / roles", ["technical project manager", "product manager", "program manager"])
    excl = askl("Exclude words", ["intern", "junior"])
    remote = ask_("Remote mode: any | remote | hybrid | onsite", "any")
    sal = ask_("Minimum salary (number or empty)", "")
    thr = ask_("Show vacancies with match >= (percent)", "60")
    mx = ask_("Max vacancies per run", "40")

    site_lines = []
    for k, label, d in SITES:
        dom = DOMAINS.get(k)
        body = "enabled: %s" % str(enabled[k]).lower() + (", domains: " + dom if dom else "")
        site_lines.append(f"  {k + ':':<10} {{ {body} }}")
    cfg = f"""# Written by scripts/setup.py. Edit by hand, or tell the agent "set X to Y". Gitignored.
profile:
  name: "{name}"
  linkedin: "{linkedin}"
  languages: {q(langs)}

paths:
  data_dir: "{data}"
  resumes_dir: "{data}/resumes"
  master_facts: "{data}/master-facts.md"

sites:
{chr(10).join(site_lines)}

search:
  locations: {q(locs)}
  keywords:  {q(kws)}
  exclude:   {q(excl)}
  remote: "{remote}"
  salary_min: {sal if sal.isdigit() else "null"}
  max_vacancies_per_run: {mx if mx.isdigit() else 40}
  match_threshold: {thr if thr.isdigit() else 60}

hh_api:
  enabled: {str(hh_api).lower()}

rules:
  require_linkedin: true
  zero_fabrication: true
  read_only_sites: true
"""
    out.write_text(cfg, encoding="utf-8")
    d = (root / data).resolve() if not pathlib.Path(data).is_absolute() else pathlib.Path(data)
    (d / "resumes").mkdir(parents=True, exist_ok=True)
    mf = d / "master-facts.md"
    if not mf.exists():
        mf.write_text(
            "# Master facts (the ONLY source for tailored resumes)\n\n"
            "Write only verified facts. One per line. Mark numbers you can prove.\n\n"
            "## Roles\n- Company, title, dates, what you did, result (number + source)\n\n"
            "## Skills\n- \n\n## Education\n- \n\n## Do not claim\n- \n",
            encoding="utf-8",
        )
    print(f"\nWrote {out}\nData folder: {d}\nPut your base resumes (md, txt or pdf) into {d / 'resumes'}")
    missing = []
    for mod in ("markdown", "weasyprint"):
        try:
            __import__(mod)
        except Exception:
            missing.append(mod)
    if missing:
        print("Optional, for PDF output: pip install " + " ".join(missing))
    print("\nNext: run the 'job-hunt-setup' agent to check the browser, log-ins and fill master-facts.md,")
    print("or go straight to: 'use stats-collector'.")


if __name__ == "__main__":
    main()
