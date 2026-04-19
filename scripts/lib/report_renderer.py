"""Render a markdown scorecard from audit results."""
from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from dimensions._plugin_base import DimensionResult  # noqa: F401
    from scripts.lib.decay_tracker import RoundSummary  # noqa: F401


def render_scorecard(skill: str,
                     results: List["DimensionResult"],
                     round_summaries: List["RoundSummary"],
                     clean_streak: int,
                     zero_rounds_required: int,
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

    # Findings, grouped by severity (informational markers excluded from this view)
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

    # Rounds — self-describing; replaces the old ambiguous sparkline.
    # Each row states its own verdict so no reader can misread a count as a round.
    lines.append("## Rounds")
    lines.append("")
    if not round_summaries:
        lines.append("_No rounds recorded._")
        lines.append("")
    else:
        lines.append("| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |")
        lines.append("|---|---|---|---|---|---|")
        for s in round_summaries:
            verdict = "🟢 CLEAN" if s.clean else "🔴 DIRTY"
            lines.append("| {} | {} | {} | {} | {} | {} |".format(
                s.round, s.structural, s.minor, s.cosmetic, s.markers, verdict,
            ))
        lines.append("")
        gate_met = "✅ PASSED" if clean_streak >= zero_rounds_required else "⏳ IN PROGRESS"
        lines.append(
            "**Clean streak (trailing):** {} round{} · **Ship gate:** {} required · {}".format(
                clean_streak,
                "" if clean_streak == 1 else "s",
                zero_rounds_required,
                gate_met,
            )
        )
        lines.append("")

    return "\n".join(lines)
