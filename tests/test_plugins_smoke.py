"""Smoke test each of the 8 dim plugins against a synthetic skill."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from dimensions._plugin_base import Finding  # noqa: E402
from scripts.lib import tree_walker  # noqa: E402
from scripts.lib.plugin_loader import discover_plugins  # noqa: E402


def _make_skill(root: str, name: str) -> str:
    path = os.path.join(root, name)
    os.makedirs(os.path.join(path, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(path, "config"), exist_ok=True)
    with open(os.path.join(path, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(
            "---\n"
            "name: " + name + "\n"
            "composable_with:\n  - \"alpha\"\n"
            "---\n\n# " + name + "\n\n## Non-goals\n\n- None.\n"
        )
    with open(os.path.join(path, "scripts", "main.py"), "w", encoding="utf-8") as fh:
        fh.write(
            "from __future__ import annotations\n\n"
            "def run(x: int) -> int:\n    return x + 1\n"
        )
    with open(os.path.join(path, "config", "settings.json"), "w", encoding="utf-8") as fh:
        json.dump({"schema_version": "0.1"}, fh)
    with open(os.path.join(path, "ARCHITECTURE.md"), "w") as fh:
        fh.write("# arch\n")
    with open(os.path.join(path, "SCHEMA.md"), "w") as fh:
        fh.write("# schema\n")
    with open(os.path.join(path, "CHANGELOG.md"), "w") as fh:
        fh.write("# changelog\n")
    return path


class TestPluginsSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = cls.tmp.name
        _make_skill(cls.root, "alpha")
        _make_skill(cls.root, "beta")
        cls.skill = tree_walker.get_skill(cls.root, "alpha")
        cls.plugins = discover_plugins()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_all_plugins_runnable(self) -> None:
        for p in self.plugins:
            findings = p.probe(self.skill)
            self.assertIsInstance(findings, list)
            for f in findings:
                self.assertIsInstance(f, Finding)

    def test_all_plugins_score_in_range(self) -> None:
        for p in self.plugins:
            findings = p.probe(self.skill)
            score = p.score(findings)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

    def test_design_audit_passes_on_well_formed_skill(self) -> None:
        design = [p for p in self.plugins if p.name == "08_design_audit"][0]
        findings = design.probe(self.skill)
        # well-formed: no major/critical findings expected
        severe = [f for f in findings if f.severity in ("major", "critical")]
        self.assertEqual(severe, [], "unexpected severe findings: {}".format(severe))

    def test_structural_flags_missing_skill_md(self) -> None:
        # Make a broken skill without SKILL.md
        broken = os.path.join(self.root, "broken")
        os.makedirs(broken, exist_ok=True)
        info = tree_walker.get_skill(self.root, "broken")
        structural = [p for p in self.plugins if p.name == "07_structural"][0]
        findings = structural.probe(info)
        kinds = {f.message for f in findings}
        self.assertTrue(any("SKILL.md" in k for k in kinds))


if __name__ == "__main__":
    unittest.main()
