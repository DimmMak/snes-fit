"""Smoke + unit tests for history_renderer."""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
sys.path.insert(0, ROOT)

from scripts.lib import history_renderer  # noqa: E402


def _write_findings(vault_dir: str, entries: list) -> None:
    os.makedirs(vault_dir, exist_ok=True)
    with open(os.path.join(vault_dir, "findings.jsonl"), "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


class TestSkillSummary(unittest.TestCase):
    def test_returns_none_when_vault_missing(self):
        self.assertIsNone(history_renderer.summarize_skill("/nonexistent/path"))

    def test_returns_none_when_findings_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            # vault dir exists but no findings.jsonl
            self.assertIsNone(history_renderer.summarize_skill(tmp))

    def test_basic_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = os.path.join(tmp, "test-skill")
            _write_findings(skill_dir, [
                {"schema_version":"0.1","timestamp_iso":"2026-04-19T10:00:00Z",
                 "round":1,"dimension":"07_structural","severity":"major",
                 "message":"x","evidence":"y"},
                {"schema_version":"0.1","timestamp_iso":"2026-04-19T10:01:00Z",
                 "round":1,"dimension":"_round_marker","severity":"informational",
                 "message":"round 1","evidence":""},
                {"schema_version":"0.1","timestamp_iso":"2026-04-19T11:00:00Z",
                 "round":2,"dimension":"_round_marker","severity":"informational",
                 "message":"round 2","evidence":""},
                {"schema_version":"0.1","timestamp_iso":"2026-04-19T12:00:00Z",
                 "round":3,"dimension":"_round_marker","severity":"informational",
                 "message":"round 3","evidence":""},
            ])
            s = history_renderer.summarize_skill(skill_dir)
            self.assertIsNotNone(s)
            self.assertEqual(s.name, "test-skill")
            self.assertEqual(s.latest_round, 3)
            self.assertEqual(s.total_rounds, 3)
            self.assertEqual(s.clean_streak, 2)  # rounds 2 + 3 are clean
            self.assertEqual(s.total_findings_all_time, 1)  # the major one


class TestSkillHistoryRender(unittest.TestCase):
    def test_empty_vault_message(self):
        out = history_renderer.render_skill_history("foo", "/nope")
        self.assertIn("No vault found", out)

    def test_render_contains_headers_and_verdicts(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = os.path.join(tmp, "foo")
            _write_findings(skill_dir, [
                {"schema_version":"0.1","timestamp_iso":"2026-04-19T10:00:00Z",
                 "round":1,"dimension":"_round_marker","severity":"informational",
                 "message":"r1","evidence":""},
            ])
            out = history_renderer.render_skill_history("foo", skill_dir)
            self.assertIn("🟣 Round", out)
            self.assertIn("🟢 CLEAN", out)


class TestFleetHistoryRender(unittest.TestCase):
    def test_empty_vault_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = history_renderer.render_fleet_history(tmp)
            self.assertIn("No audit history yet", out)

    def test_fleet_with_mixed_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Ship-ready skill
            ready_dir = os.path.join(tmp, "ready-skill")
            _write_findings(ready_dir, [
                {"schema_version":"0.1","timestamp_iso":"2026-04-19T10:00:00Z",
                 "round":1,"dimension":"_round_marker","severity":"informational",
                 "message":"r1","evidence":""},
                {"schema_version":"0.1","timestamp_iso":"2026-04-19T11:00:00Z",
                 "round":2,"dimension":"_round_marker","severity":"informational",
                 "message":"r2","evidence":""},
            ])
            # Dirty skill
            dirty_dir = os.path.join(tmp, "dirty-skill")
            _write_findings(dirty_dir, [
                {"schema_version":"0.1","timestamp_iso":"2026-04-19T10:00:00Z",
                 "round":1,"dimension":"07_structural","severity":"major",
                 "message":"broken","evidence":"x"},
            ])
            out = history_renderer.render_fleet_history(tmp)
            self.assertIn("ready-skill", out)
            self.assertIn("dirty-skill", out)
            self.assertIn("Ship-ready today:** 1 / 2", out)  # bold markdown around label
            # Ready skill should come first (sorted ship-ready first)
            ready_idx = out.find("ready-skill")
            dirty_idx = out.find("dirty-skill")
            self.assertLess(ready_idx, dirty_idx)


if __name__ == "__main__":
    unittest.main()
