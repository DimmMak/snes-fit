"""Aggregate per-dimension scores into an overall 0-100 grade."""
from __future__ import annotations

from typing import Dict, List, Optional

try:
    # Support both package-relative import and direct script import.
    from dimensions._plugin_base import DimensionResult  # type: ignore
except Exception:  # pragma: no cover
    DimensionResult = None  # type: ignore


SHIP_THRESHOLD: int = 80


def calculate_score(dimension_results: List["DimensionResult"],
                    weights: Optional[Dict[str, float]] = None) -> int:
    """Weighted mean of per-dim scores, mapped into 0-100 and clamped."""
    if not dimension_results:
        return 0
    if weights is None:
        weights = {}
    total_weight = 0.0
    weighted_sum = 0.0
    for r in dimension_results:
        w = float(weights.get(r.dimension, 1.0))
        total_weight += w
        weighted_sum += w * float(r.score)
    if total_weight <= 0:
        return 0
    raw = (weighted_sum / total_weight) * 100.0
    # Clamp [0, 100] — NON_GOAL #9 forbids overflow.
    clamped = max(0, min(100, int(round(raw))))
    return clamped


def grade(score: int) -> str:
    """Letter grade from integer score."""
    if score >= 95:
        return "A+"
    if score >= 90:
        return "A"
    if score >= 85:
        return "B+"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def is_ship_ready(score: int) -> bool:
    return score >= SHIP_THRESHOLD
