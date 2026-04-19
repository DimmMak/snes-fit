"""Cumulative cost ceiling for a single audit run.

Reads `config/thresholds.json` for `max_cost_usd_per_run` (default 5.0).
Plugins consult `CostGuard.can_spend(estimate)` before each LLM call and
`record(actual)` afterward. Once exceeded, remaining LLM dims should
short-circuit to UNKNOWN rather than crash.
"""
from __future__ import annotations

import json
import os
from typing import Optional


class CostBudgetExceeded(Exception):
    """Raised when an attempted charge would overflow the budget."""


class CostGuard:
    def __init__(self, max_usd: float = 5.0):
        self.max_usd = float(max_usd)
        self._spent = 0.0
        self._tripped = False

    @classmethod
    def from_config(cls, thresholds_path: Optional[str] = None) -> "CostGuard":
        if thresholds_path is None:
            here = os.path.dirname(os.path.abspath(__file__))
            thresholds_path = os.path.abspath(
                os.path.join(here, "..", "..", "config", "thresholds.json")
            )
        try:
            with open(thresholds_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            max_usd = float(data.get("max_cost_usd_per_run", 5.0))
        except (OSError, json.JSONDecodeError, ValueError):
            max_usd = 5.0
        return cls(max_usd=max_usd)

    @property
    def spent_usd(self) -> float:
        return round(self._spent, 6)

    @property
    def remaining_usd(self) -> float:
        return max(0.0, round(self.max_usd - self._spent, 6))

    @property
    def tripped(self) -> bool:
        return self._tripped

    def can_spend(self, estimate_usd: float) -> bool:
        return (self._spent + float(estimate_usd)) <= self.max_usd

    def record(self, actual_usd: float) -> None:
        self._spent += float(actual_usd)
        if self._spent > self.max_usd:
            self._tripped = True

    def charge(self, estimate_usd: float) -> None:
        """Pre-check + record. Raises CostBudgetExceeded if over."""
        if not self.can_spend(estimate_usd):
            self._tripped = True
            raise CostBudgetExceeded(
                "Spend {:.6f} would exceed budget {:.2f} (already ${:.6f})".format(
                    estimate_usd, self.max_usd, self._spent,
                )
            )
        self.record(estimate_usd)
