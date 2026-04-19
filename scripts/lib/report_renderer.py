"""Render a markdown scorecard from audit results."""
from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from dimensions._plugin_base import DimensionResult  # noqa: F401


def _decay_ascii(curve: List[int]) -> str:
    """Render the decay curve as a tiny ASCII sparkline."""
    if not curve:
        return "(no rounds recorded)"
    bars = "▁▂▃▄▅▆▇█"
    peak = max(curve) or 1
    out = []
    for v in curve:
        idx = min(len(bars) - 1, int(round((v / peak) * (len(bars) - 1))))
        out.append(bars[idx])
    return "".join(out) + "  (" + " ".join(str(v) for v in curve) + ")"


def render_scorecard(skill: str,
                     results: List["DimensionResult"],
                     decay_curve: List[int],
                     score: int,
                     grade: str,
                     ship_ready: Optional[bool] = None) -> str:
    """Return a markdown scorecard string."""
    lines: List[str] = []
    lines.append("# .auto-test scorecard — {}".format(skill))
    lines.append("")
    lines.append("**Overall score:** {}/100  |  **Grade:** {}".format(score, grade))
    if ship_ready is not None:
        lines.append("**Ship-ready (decay rule):** {}".format("YES" if ship_ready else "NO"))
    lines.append("")

    # Per-dimension table
    lines.append("## Per-dimension results")
    lines.append("")
    lines.append("| 🟣 Dimension | 🟣 Score | 🟣 Findings | 🟣 Verdict |")
    lines.append("|---|---|---|---|")
    for r in results:
        verdict = "PASS" if r.passed else "FAIL"
        lines.append("| {} | {:.2f} | {} | {} |".format(
            r.dimension, r.score, len(r.findings), verdict
        ))
    lines.append("")

    # Findings, grouped by severity
    lines.append("## Findings")
    lines.append("")
    severities = ("critical", "major", "minor", "cosmetic")
    flat = [f for r in results for f in r.findings]
    if not flat:
        lines.append("_No findings._")
        lines.append("")
    else:
        for sev in severities:
            batch = [f for f in flat if f.severity == sev]
            if not batch:
                continue
            lines.append("### {} ({})".format(sev.capitalize(), len(batch)))
            lines.append("")
            lines.append("| 🟣 Dimension | 🟣 Message | 🟣 Evidence |")
            lines.append("|---|---|---|")
            for f in batch:
                msg = f.message.replace("|", "\\|")
                ev = f.evidence.replace("|", "\\|")
                if len(ev) > 120:
                    ev = ev[:117] + "..."
                lines.append("| {} | {} | {} |".format(f.dimension, msg, ev))
            lines.append("")

    # Decay curve
    lines.append("## Decay curve")
    lines.append("")
    lines.append("```")
    lines.append(_decay_ascii(decay_curve))
    lines.append("```")
    lines.append("")

    return "\n".join(lines)
