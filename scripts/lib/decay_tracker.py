"""Decay tracker — implements the stress-test cadence stopping rule.

Ship when the last N rounds are all "zero" rounds:
  - zero structural (critical/major) findings
  - <= 1 cosmetic finding
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, List


STRUCTURAL = ("critical", "major")


@dataclass
class Finding:
    schema_version: str
    timestamp_iso: str
    round: int
    dimension: str
    severity: str
    message: str
    evidence: str


def load_findings(vault_path: str) -> List[Finding]:
    """Read `vault_path/findings.jsonl` (or treat `vault_path` as the file itself)."""
    path = vault_path
    if os.path.isdir(vault_path):
        path = os.path.join(vault_path, "findings.jsonl")
    out: List[Finding] = []
    if not os.path.isfile(path):
        return out
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                # parse-tolerant
                continue
            out.append(Finding(
                schema_version=str(d.get("schema_version", "0.1")),
                timestamp_iso=str(d.get("timestamp_iso", "")),
                round=int(d.get("round", 1)),
                dimension=str(d.get("dimension", "")),
                severity=str(d.get("severity", "minor")),
                message=str(d.get("message", "")),
                evidence=str(d.get("evidence", "")),
            ))
    return out


def group_by_round(findings: List[Finding]) -> Dict[int, List[Finding]]:
    """Group findings by their .round field."""
    groups: Dict[int, List[Finding]] = {}
    for f in findings:
        groups.setdefault(f.round, []).append(f)
    return groups


def _is_zero_round(fs: List[Finding]) -> bool:
    structural = sum(1 for f in fs if f.severity in STRUCTURAL)
    cosmetic = sum(1 for f in fs if f.severity == "cosmetic")
    return structural == 0 and cosmetic <= 1


def is_ship_ready(findings_by_round: Dict[int, List[Finding]],
                  zero_rounds_required: int = 2) -> bool:
    """True iff the last `zero_rounds_required` rounds are all zero rounds."""
    if not findings_by_round:
        return False
    rounds_sorted = sorted(findings_by_round.keys())
    if len(rounds_sorted) < zero_rounds_required:
        return False
    tail = rounds_sorted[-zero_rounds_required:]
    return all(_is_zero_round(findings_by_round[r]) for r in tail)


def decay_curve(findings_by_round: Dict[int, List[Finding]]) -> List[int]:
    """Return bugs-per-round as a list in round order (for report graphs)."""
    if not findings_by_round:
        return []
    max_round = max(findings_by_round.keys())
    return [len(findings_by_round.get(r, [])) for r in range(1, max_round + 1)]


@dataclass
class RoundSummary:
    round: int
    structural: int  # critical + major
    cosmetic: int
    minor: int
    markers: int  # informational
    clean: bool  # structural == 0 and cosmetic <= 1


def summarize_rounds(findings_by_round: Dict[int, List[Finding]]) -> List[RoundSummary]:
    """One row per round with explicit CLEAN/DIRTY status.

    Output is self-describing so readers (humans or LLMs) cannot misread a
    raw count as a round count. Each row states its own verdict.
    """
    out: List[RoundSummary] = []
    for r in sorted(findings_by_round.keys()):
        fs = findings_by_round[r]
        structural = sum(1 for f in fs if f.severity in STRUCTURAL)
        cosmetic = sum(1 for f in fs if f.severity == "cosmetic")
        minor = sum(1 for f in fs if f.severity == "minor")
        markers = sum(1 for f in fs if f.severity == "informational")
        clean = structural == 0 and cosmetic <= 1
        out.append(RoundSummary(r, structural, cosmetic, minor, markers, clean))
    return out


def clean_streak(summaries: List[RoundSummary]) -> int:
    """Count trailing consecutive clean rounds (0 if newest round is dirty)."""
    streak = 0
    for s in reversed(summaries):
        if s.clean:
            streak += 1
        else:
            break
    return streak


def next_round_id(findings_by_round: Dict[int, List[Finding]]) -> int:
    """Auto-increment round: one more than the max existing round, or 1."""
    if not findings_by_round:
        return 1
    return max(findings_by_round.keys()) + 1
