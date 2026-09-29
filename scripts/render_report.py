#!/usr/bin/env python3
"""Render stats.json to a self-contained HTML report. No network, no dependencies."""
import json, sys, html, collections

def esc(x): return html.escape(str(x if x is not None else ""))

def main(src, dst):
    d = json.load(open(src, encoding="utf-8"))
    apps = d.get("applications", [])
    status_order = ["offer", "interview", "invited", "viewed", "not_viewed", "rejected"]
    colors = {"offer": "#2e7d32", "interview": "#43a047", "invited": "#7cb342",
              "viewed": "#f9a825", "not_viewed": "#9e9e9e", "rejected": "#c62828"}
    cnt = collections.Counter(a.get("status", "not_viewed") for a in apps)
    total = len(apps) or 1
    by_res = collections.defaultdict(lambda: collections.Counter())
    for a in apps:
        by_res[a.get("resume") or "unknown"][a.get("status", "not_viewed")] += 1
    by_site = collections.Counter(a.get("site", "?") for a in apps)

    bar = "".join(
        f'<div style="width:{cnt[s]*100/total:.1f}%;background:{colors[s]}" title="{s}: {cnt[s]}"></div>'
        for s in status_order if cnt[s])
    legend = "".join(f'<span><i style="background:{colors[s]}"></i>{s} {cnt[s]}</span>'
                     for s in status_order if cnt[s])

    res_rows = ""
    for r, c in sorted(by_res.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(c.values()); good = c["interview"] + c["invited"] + c["offer"]
        res_rows += (f"<tr><td>{esc(r)}</td><td>{n}</td><td>{good}</td>"
                     f"<td>{good*100/n:.0f}%</td><td>{c['rejected']}</td></tr>")

    app_rows = ""
    for a in sorted(apps, key=lambda x: x.get("date", ""), reverse=True):
        s = a.get("status", "")
        app_rows += (f'<tr><td>{esc(a.get("date"))}</td><td>{esc(a.get("site"))}</td>'
                     f'<td>{esc(a.get("company"))}</td><td>{esc(a.get("role"))}</td>'
                     f'<td><b style="color:{colors.get(s,"#333")}">{esc(s)}</b></td>'
                     f'<td>{esc(a.get("resume"))}</td><td>{esc(a.get("why") or a.get("note"))}</td></tr>')

    li = lambda items: "".join(f"<li>{esc(i)}</li>" for i in items) or "<li>none</li>"
    snaps = "".join(f"<tr><td>{esc(s.get('date'))}</td><td>{esc(json.dumps(s.get('totals',{}), ensure_ascii=False))}</td></tr>"
                    for s in d.get("snapshots", [])[-10:])

    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Job search report</title>
<style>
body{{font-family:system-ui,Arial,sans-serif;margin:0;background:#f5f6f8;color:#1c1e21}}
main{{max-width:1100px;margin:0 auto;padding:24px}}
h1{{margin:0 0 4px}} h2{{margin:28px 0 8px;font-size:1.1rem}}
.card{{background:#fff;border-radius:10px;padding:16px;box-shadow:0 1px 3px #0001;margin-bottom:16px}}
.kpi{{display:flex;gap:12px;flex-wrap:wrap}} .kpi div{{flex:1;min-width:120px;background:#fff;border-radius:10px;padding:14px;box-shadow:0 1px 3px #0001}}
.kpi b{{font-size:1.8rem;display:block}}
.bar{{display:flex;height:22px;border-radius:6px;overflow:hidden;margin:8px 0}}
.legend span{{margin-right:14px;font-size:.85rem}} .legend i{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px}}
table{{width:100%;border-collapse:collapse;font-size:.88rem}} th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid #eee;vertical-align:top}}
th{{background:#fafafa}} ul{{margin:6px 0 0 18px}} .muted{{color:#6b7280;font-size:.85rem}}
</style></head><body><main>
<h1>Job search report</h1><div class="muted">Updated {esc(d.get('updated'))} · sites: {esc(', '.join(f'{k} {v}' for k,v in by_site.items()))}</div>
<h2>Summary</h2>
<div class="kpi"><div><b>{len(apps)}</b>tracked applications</div>
<div><b>{cnt['interview']+cnt['invited']+cnt['offer']}</b>invites, interviews, offers</div>
<div><b>{cnt['rejected']}</b>rejections</div>
<div><b>{cnt['viewed']+cnt['not_viewed']}</b>no answer yet</div>
<div><b>{(cnt['interview']+cnt['invited']+cnt['offer'])*100/total:.0f}%</b>positive rate</div></div>
<div class="card"><div class="bar">{bar}</div><div class="legend">{legend}</div>
<div class="muted">All-time applications reported by the site: {esc(d.get('totals',{}).get('applications_all_time','n/a'))}. Only visible ones are tracked.</div></div>
<h2>Which resume works</h2><div class="card"><table><tr><th>Resume</th><th>Sent</th><th>Positive</th><th>Rate</th><th>Rejected</th></tr>{res_rows}</table></div>
<div class="card"><h2 style="margin-top:0">Why it may not work (hypotheses)</h2><ul>{li(d.get('insights',[]))}</ul></div>
<div class="card"><h2 style="margin-top:0">Profile issues to fix</h2><ul>{li(d.get('profile_issues',[]))}</ul></div>
<h2>Applications</h2><div class="card" style="overflow-x:auto"><table><tr><th>Date</th><th>Site</th><th>Company</th><th>Role</th><th>Status</th><th>Resume</th><th>Note / hypothesis</th></tr>{app_rows}</table></div>
<h2>History</h2><div class="card"><table><tr><th>Date</th><th>Totals</th></tr>{snaps}</table></div>
</main></body></html>"""
    open(dst, "w", encoding="utf-8").write(page)
    print("wrote", dst)

if __name__ == "__main__":
    if len(sys.argv) != 3: sys.exit("usage: render_report.py stats.json report.html")
    main(*sys.argv[1:])
