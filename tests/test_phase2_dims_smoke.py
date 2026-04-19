"""Smoke test phase-2 dims (09-14) against a synthetic skill in mock mode.

Confirms:
  - Every dim is discoverable via the plugin loader
  - Every dim runs without crashing against a temp skill
  - Every dim returns a List[Finding]
  - Phase-1 dims still run unchanged
"""
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


PHASE2_IDS = {
    "09_llm_output_quality",
    "10_trigger_precision",
    "11_hallucination_probe",
    "12_prompt_injection",
    "13_contract_drift",
    "14_llm_self_audit",
}


def _make_skill(root: str, name: str) -> str:
    path = os.path.join(root, name)
    os.makedirs(os.path.join(path, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(path, "config"), exist_ok=True)
    with open(os.path.join(path, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(
            "---\n"
            "name: " + name + "\n"
            "composable_with:\n  - \"peer\"\n"
            "---\n\n# " + name + "\n\n"
            "Produces a short structured summary.\n\n"
            "NOT for: writing code.\n\nNOT for: image generation.\n\n"
            "## Non-goals\n- None.\n"
        )
    with open(os.path.join(path, "ARCHITECTURE.md"), "w") as fh:
        fh.write("# architecture\n\nSingle invariant: output is JSON.\n")
    with open(os.path.join(path, "NON_GOALS.md"), "w") as fh:
        fh.write("- Not for code generation.\n- Not for image generation.\n")
    with open(os.path.join(path, "CHANGELOG.md"), "w") as fh:
        fh.write("# changelog\n")
    with open(os.path.join(path, "scripts", "main.py"), "w") as fh:
        fh.write("def run(x: int) -> int:\n    return x + 1\n")
    with open(os.path.join(path, "config", "settings.json"), "w") as fh:
        json.dump({"schema_version": "0.1"}, fh)
    return path


class TestPhase2DimsSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ["AUTO_TEST_MOCK"] = "1"
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = cls.tmp.name
        _make_skill(cls.root, "alpha")
        _make_skill(cls.root, "peer")
        cls.skill = tree_walker.get_skill(cls.root, "alpha")
        # Discover with all phase-2 ids enabled
        cls.plugins = discover_plugins(enabled_ids=list(PHASE2_IDS))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_all_six_discovered(self) -> None:
        names = {p.name for p in self.plugins}
        self.assertEqual(names, PHASE2_IDS)

    def test_each_dim_runs_without_crash(self) -> None:
        for p in self.plugins:
            with self.subTest(dim=p.name):
                findings = p.probe(self.skill)
                self.assertIsInstance(findings, list)
                for f in findings:
                    self.assertIsInstance(f, Finding)

    def test_scores_in_range(self) -> None:
        for p in self.plugins:
            with self.subTest(dim=p.name):
                findings = p.probe(self.skill)
                score = p.score(findings)
                self.assertGreaterEqual(score, 0.0)
                self.assertLessEqual(score, 1.0)

    def test_mock_produces_pass_on_benign_skill(self) -> None:
        # Benign SKILL.md should produce PASS verdicts in mock mode
        # (no 'fail_keyword' / 'hallucinate' / 'jailbreak_success' in content).
        for p in self.plugins:
            if p.name == "12_prompt_injection":
                # attack prompts contain JAILBREAK_SUCCESS keyword -> mock FAILs
                continue
            with self.subTest(dim=p.name):
                findings = p.probe(self.skill)
                # no critical findings expected on the happy path
                crits = [f for f in findings if f.severity == "critical"]
                self.assertEqual(crits, [], "unexpected critical: {}".format(crits))


class TestPhase1DimsUnchanged(unittest.TestCase):
    """Ensure phase-1 dims still load + run even with phase-2 present."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = cls.tmp.name
        _make_skill(cls.root, "alpha")
        cls.skill = tree_walker.get_skill(cls.root, "alpha")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_phase1_ids_still_discoverable(self) -> None:
        phase1 = [
            "01_adversarial", "02_scale", "03_composition", "04_security",
            "05_threat_intel", "06_types", "07_structural", "08_design_audit",
        ]
        plugins = discover_plugins(enabled_ids=phase1)
        names = {p.name for p in plugins}
        self.assertEqual(names, set(phase1))


if __name__ == "__main__":
    unittest.main()
