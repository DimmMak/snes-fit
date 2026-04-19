"""CostGuard enforces max_cost_usd_per_run."""
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

from scripts.lib.cost_guard import CostBudgetExceeded, CostGuard  # noqa: E402


class TestCostGuard(unittest.TestCase):
    def test_initial_state(self) -> None:
        g = CostGuard(max_usd=1.0)
        self.assertEqual(g.spent_usd, 0.0)
        self.assertEqual(g.remaining_usd, 1.0)
        self.assertFalse(g.tripped)

    def test_can_spend_boundaries(self) -> None:
        g = CostGuard(max_usd=1.0)
        self.assertTrue(g.can_spend(0.5))
        self.assertTrue(g.can_spend(1.0))
        self.assertFalse(g.can_spend(1.01))

    def test_record_accumulates(self) -> None:
        g = CostGuard(max_usd=2.0)
        g.record(0.5)
        g.record(0.75)
        self.assertAlmostEqual(g.spent_usd, 1.25, places=6)
        self.assertAlmostEqual(g.remaining_usd, 0.75, places=6)

    def test_charge_raises_when_over(self) -> None:
        g = CostGuard(max_usd=1.0)
        g.record(0.9)
        with self.assertRaises(CostBudgetExceeded):
            g.charge(0.2)
        self.assertTrue(g.tripped)

    def test_record_trips_flag(self) -> None:
        g = CostGuard(max_usd=1.0)
        g.record(1.5)
        self.assertTrue(g.tripped)

    def test_from_config_reads_json(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump({"max_cost_usd_per_run": 2.5}, fh)
            path = fh.name
        try:
            g = CostGuard.from_config(path)
            self.assertEqual(g.max_usd, 2.5)
        finally:
            os.unlink(path)

    def test_from_config_fallback(self) -> None:
        g = CostGuard.from_config("/nonexistent/path.json")
        self.assertEqual(g.max_usd, 5.0)


if __name__ == "__main__":
    unittest.main()
