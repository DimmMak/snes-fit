from __future__ import annotations

import os
import sys
import unittest

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from dimensions._plugin_base import DimensionPlugin, Finding  # noqa: E402


class _Probe(DimensionPlugin):
    name = "_probe"

    def probe(self, target):  # pragma: no cover - unused
        return []


class TestDefaultScore(unittest.TestCase):
    def setUp(self) -> None:
        self.p = _Probe()

    def _f(self, sev: str) -> Finding:
        return Finding(dimension="_probe", severity=sev, message="m", evidence="e")

    def test_no_findings_is_perfect(self) -> None:
        self.assertEqual(self.p.score([]), 1.0)

    def test_critical_zeroes_score(self) -> None:
        self.assertEqual(self.p.score([self._f("critical")]), 0.0)

    def test_major_penalty(self) -> None:
        self.assertAlmostEqual(self.p.score([self._f("major")]), 0.8)

    def test_minor_penalty(self) -> None:
        self.assertAlmostEqual(self.p.score([self._f("minor")]), 0.95)

    def test_cosmetic_penalty_exists(self) -> None:
        # Regression: cosmetic used to score 0 penalty, misaligned with decay rule.
        self.assertAlmostEqual(self.p.score([self._f("cosmetic")]), 0.99)

    def test_cosmetic_stacks(self) -> None:
        findings = [self._f("cosmetic") for _ in range(5)]
        self.assertAlmostEqual(self.p.score(findings), 0.95)

    def test_mixed(self) -> None:
        # 1 major (-0.2) + 2 minor (-0.1) + 3 cosmetic (-0.03) = 0.67
        findings = [self._f("major"),
                    self._f("minor"), self._f("minor"),
                    self._f("cosmetic"), self._f("cosmetic"), self._f("cosmetic")]
        self.assertAlmostEqual(self.p.score(findings), 0.67)


if __name__ == "__main__":
    unittest.main()
