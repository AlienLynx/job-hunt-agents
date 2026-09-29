#!/usr/bin/env python3
"""md -> html -> pdf (needs: pip install markdown weasyprint)."""
import sys, pathlib
try:
    import markdown, weasyprint
except ImportError:
    sys.exit("install first: pip install markdown weasyprint")
src = pathlib.Path(sys.argv[1]); accent = sys.argv[2] if len(sys.argv) > 2 else "#1f4e79"
body = markdown.markdown(src.read_text(encoding="utf-8"), extensions=["extra"])
css = f"""@page{{size:A4;margin:12mm 15mm}}body{{font-family:Arial,sans-serif;font-size:9.5pt;line-height:1.3;color:#111}}
h1{{font-size:17pt;margin:0}}h1+p{{font-size:11pt;font-weight:bold;color:{accent};margin:0 0 2pt}}
h2{{font-size:10.5pt;text-transform:uppercase;letter-spacing:.5pt;color:{accent};border-bottom:1.2px solid {accent};margin:8pt 0 4pt}}
p{{margin:0 0 4pt}}ul{{margin:2pt 0 4pt;padding-left:13pt}}li{{margin-bottom:1.5pt}}strong{{color:{accent}}}"""
html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'
out = src.with_suffix(".pdf"); weasyprint.HTML(string=html).write_pdf(out); print("wrote", out)
