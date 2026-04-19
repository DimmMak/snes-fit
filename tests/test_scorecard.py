from __future__ import annotations

import os
import sys
import unittest

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from dimensions._plugin_base import DimensionResult, Finding  # noqa: E402
from scripts.lib import scorecard  # noqa: E402


class TestScorecard(unittest.TestCase):
    def test_empty_is_zero(self) -> None:
        self.assertEqual(scorecard.calculate_score([]), 0)

    def test_perfect_scores_to_100(self) -> None:
        results = [
            DimensionResult(dimension="a", score=1.0, findings=[], passed=True),
            DimensionResult(dimension="b", score=1.0, findings=[], passed=True),
        ]
        self.assertEqual(scorecard.calculate_score(results), 100)

    def test_clamped_to_100(self) -> None:
        # Out-of-range scores get clamped (defensive)
        results = [DimensionResult(dimension="a", score=5.0, findings=[], passed=True)]
        s = scorecard.calculate_score(results)
        self.assertLessEqual(s, 100)

    def test_grade_boundaries(self) -> None:
        self.assertEqual(scorecard.grade(100), "A+")
        self.assertEqual(scorecard.grade(90), "A")
        self.assertEqual(scorecard.grade(85), "B+")
        self.assertEqual(scorecard.grade(80), "B")
        self.assertEqual(scorecard.grade(70), "C")
        self.assertEqual(scorecard.grade(60), "D")
        self.assertEqual(scorecard.grade(0), "F")

    def test_weighted(self) -> None:
        results = [
            DimensionResult(dimension="a", score=1.0, findings=[], passed=True),
            DimensionResult(dimension="b", score=0.0, findings=[], passed=False),
        ]
        # Equal weights -> 50
        self.assertEqual(scorecard.calculate_score(results), 50)
        # Weight a=3, b=1 -> 75
        self.assertEqual(scorecard.calculate_score(results, weights={"a": 3.0, "b": 1.0}), 75)


if __name__ == "__main__":
    unittest.main()
