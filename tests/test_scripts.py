import argparse, json, os, pathlib, shutil, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
PY = sys.executable


def run(*args):
    return subprocess.run([PY, *map(str, args)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


class Scripts(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_match_ranks_best_resume(self):
        (self.tmp / "r.json").write_text(json.dumps([
            {"id": "pm", "file": "none", "terms": ["jira", "scrum", "roadmap"]},
            {"id": "hw", "file": "none", "terms": ["pcb", "firmware"]}]))
        (self.tmp / "v.json").write_text(json.dumps([
            {"id": "1", "title": "PM", "requirements": ["Jira", "Scrum", "roadmap"]}]))
        p = run("scripts/match.py", "--resumes", self.tmp / "r.json", "--vacancies", self.tmp / "v.json", "--out", self.tmp / "o.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads((self.tmp / "o.json").read_text())
        self.assertEqual(out[0]["best_resume"], "pm")
        self.assertEqual(out[0]["match_pre"], 100)

    def test_check_resume_flags_problems(self):
        facts = self.tmp / "facts.md"
        facts.write_text("Led 12 people, cut cost 30%")
        cfg = self.tmp / "c.yaml"
        cfg.write_text('profile:\n  linkedin: "linkedin.com/in/x"\npaths:\n  master_facts: "%s"\nrules:\n  require_linkedin: true\n' % facts.as_posix())
        bad = self.tmp / "bad.md"
        bad.write_text("Passionate leader, grew revenue 99% — wow", encoding="utf-8")
        good = self.tmp / "good.md"
        good.write_text("linkedin.com/in/x\nLed 12 people, cut cost 30%", encoding="utf-8")
        pb = run("scripts/check_resume.py", bad, "--config", cfg)
        self.assertEqual(pb.returncode, 1)
        for s in ("linkedin", "99", "passionate", "long dash"):
            self.assertIn(s, pb.stdout.lower())
        self.assertEqual(run("scripts/check_resume.py", good, "--config", cfg).returncode, 0)

    def test_render_report(self):
        out = self.tmp / "r.html"
        p = run("scripts/render_report.py", "examples/stats.example.json", out)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Acme Robotics", out.read_text(encoding="utf-8"))

    def test_setup_defaults_writes_config_and_data(self):
        cfg = self.tmp / "config.local.yaml"
        existed = (ROOT / "jobhunt-data").exists()
        p = run("scripts/setup.py", "--defaults", "--out", cfg)
        self.assertEqual(p.returncode, 0, p.stderr)
        t = cfg.read_text(encoding="utf-8")
        for k in ("profile:", "sites:", "praca_by:", "habr_career:", "hh_api:", "require_linkedin: true"):
            self.assertIn(k, t)
        if not existed:
            shutil.rmtree(ROOT / "jobhunt-data", ignore_errors=True)

    def test_build_is_idempotent(self):
        files = list((ROOT / ".claude/agents").glob("*.md")) + list((ROOT / "skills").glob("*/SKILL.md"))
        before = {p: p.read_bytes() for p in files}
        self.assertEqual(run("scripts/build.py").returncode, 0)
        after = {p: p.read_bytes() for p in files}
        self.assertEqual(before, after, "generated agents/skills are stale: run scripts/build.py and commit")

    def test_all_agents_use_cheapest_model_and_common_rules(self):
        agents = list((ROOT / ".claude/agents").glob("*.md"))
        self.assertGreaterEqual(len(agents), 4)
        for f in agents:
            t = f.read_text(encoding="utf-8")
            self.assertIn("model: haiku", t, f.name)
            self.assertNotIn("{{COMMON}}", t, f.name)
            self.assertIn("Never type passwords", t, f.name)

    def test_manifests_valid_and_paths_exist(self):
        for n in ("marketplace.json", "plugin.json"):
            json.loads((ROOT / ".claude-plugin" / n).read_text(encoding="utf-8"))
        pj = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        for p in pj["agents"] + pj["skills"]:
            self.assertTrue((ROOT / p).exists(), p)

    def test_no_personal_data_in_tracked_files(self):
        r = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            self.skipTest("not a git checkout")
        for f in r.stdout.split():
            if f.endswith((".py", ".md", ".yaml", ".json", ".sh", ".example")) and not f.startswith("tests/"):
                t = (ROOT / f).read_text(encoding="utf-8", errors="ignore")
                for bad in ("github_pat_", "@outlook.com", "@gmail.com", "Chuev", "Чуев"):
                    self.assertNotIn(bad, t, "%s in %s" % (bad, f))

    def test_env_loader_does_not_override_real_env(self):
        import jobhunt_env
        f = self.tmp / ".env"
        f.write_text('A_TEST_KEY="from_file"\nB_TEST_KEY=2\n# c=3\n')
        os.environ["JOBHUNT_ENV"] = str(f)
        os.environ["A_TEST_KEY"] = "real"
        try:
            jobhunt_env.load()
            self.assertEqual(os.environ["A_TEST_KEY"], "real")
            self.assertEqual(os.environ["B_TEST_KEY"], "2")
        finally:
            for k in ("JOBHUNT_ENV", "A_TEST_KEY", "B_TEST_KEY"):
                os.environ.pop(k, None)

    def test_hh_api_maps_negotiations_without_network(self):
        import hh_api
        pages = {0: {"pages": 1, "items": [
            {"id": "9", "created_at": "2026-09-21T10:00:00+0300", "state": {"id": "discard"},
             "resume": {"title": "PM-general"}, "vacancy": {"name": "PM", "employer": {"name": "Acme"}}},
            {"id": "8", "created_at": "2026-09-20T10:00:00+0300", "state": {"id": "response"}, "viewed_by_opponent": False,
             "resume": {"title": "Product"}, "vacancy": {"name": "PO", "employer": {"name": "Bee"}}}]}}
        orig = hh_api.get
        hh_api.get = lambda path, host, params=None: pages[params["page"]]
        try:
            out = self.tmp / "rows.json"
            hh_api.cmd_negotiations(argparse.Namespace(host="rabota.by", out=str(out)))
        finally:
            hh_api.get = orig
        rows = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(rows[0]["status"], "rejected")
        self.assertEqual(rows[0]["resume"], "PM-general")
        self.assertEqual(rows[1]["status"], "not_viewed")
        self.assertEqual(rows[0]["site"], "rabota_by")


if __name__ == "__main__":
    unittest.main()
