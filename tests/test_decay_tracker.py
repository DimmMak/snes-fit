from __future__ import annotations

import os
import sys
import tempfile
import unittest

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.lib import decay_tracker, regression_vault  # noqa: E402


class TestDecayTracker(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = self.tmp.name

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _add(self, round_num: int, severity: str) -> None:
        regression_vault.append_finding(self.vault, {
            "schema_version": "0.1",
            "timestamp_iso": "2026-04-19T00:00:00Z",
            "round": round_num,
            "dimension": "t",
            "severity": severity,
            "message": "m",
            "evidence": "e",
        })

    def test_empty_not_ship_ready(self) -> None:
        self.assertFalse(decay_tracker.is_ship_ready({}, zero_rounds_required=2))

    def test_ship_ready_two_clean_rounds(self) -> None:
        self._add(1, "major")
        self._add(2, "cosmetic")
        self._add(3, "cosmetic")
        findings = decay_tracker.load_findings(self.vault)
        groups = decay_tracker.group_by_round(findings)
        self.assertTrue(decay_tracker.is_ship_ready(groups, zero_rounds_required=2))

    def test_not_ship_if_last_round_has_major(self) -> None:
        self._add(1, "cosmetic")
        self._add(2, "major")
        groups = decay_tracker.group_by_round(decay_tracker.load_findings(self.vault))
        self.assertFalse(decay_tracker.is_ship_ready(groups, zero_rounds_required=2))

    def test_decay_curve_monotone(self) -> None:
        for r, sev in [(1, "major"), (1, "major"), (2, "minor"), (3, "cosmetic")]:
            self._add(r, sev)
        groups = decay_tracker.group_by_round(decay_tracker.load_findings(self.vault))
        curve = decay_tracker.decay_curve(groups)
        self.assertEqual(curve, [2, 1, 1])

    def test_parse_tolerant(self) -> None:
        # Write one bad line directly and one good line
        path = os.path.join(self.vault, "findings.jsonl")
        os.makedirs(self.vault, exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("not json\n")
        self._add(1, "minor")
        findings = decay_tracker.load_findings(self.vault)
        self.assertEqual(len(findings), 1)


if __name__ == "__main__":
    unittest.main()
