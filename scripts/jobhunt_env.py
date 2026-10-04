"""Tiny .env loader for scripts (no dependencies). Agents must never read or print this file.
Search order: $JOBHUNT_ENV, ./.env, ~/.jobhunt/.env. Real environment variables win over the file.
"""
import os, pathlib


def load():
    cands = [os.environ.get("JOBHUNT_ENV"), ".env", "~/.jobhunt/.env"]
    for c in cands:
        if not c:
            continue
        p = pathlib.Path(c).expanduser()
        if p.is_file():
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return str(p)
    return None
