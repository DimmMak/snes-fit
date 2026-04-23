"""Render per-skill and fleet-wide audit history as markdown.

Reads from vault/<skill>/findings.jsonl (the authoritative source).
No external deps. Every table uses 🟣-only headers per memory rules.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from scripts.lib import decay_tracker


@dataclass
class SkillSummary:
    """One-row summary of a skill's latest audit state."""
    name: str
    latest_round: int
    total_rounds: int
    latest_structural: int
    latest_cosmetic: int
    latest_minor: int
    latest_clean: bool
    clean_streak: int
    ship_ready: bool  # clean_streak >= zero_rounds_required
    # best + worst rounds for context
    total_findings_all_time: int


def summarize_skill(vault_dir: str,
                    zero_rounds_required: int = 2) -> Optional[SkillSummary]:
    """Build a SkillSummary from the findings.jsonl of one skill.

    Returns None if the vault has no findings at all (skill never audited).
    """
    if not os.path.isdir(vault_dir):
        return None
    name = os.path.basename(os.path.normpath(vault_dir))
    findings = decay_tracker.load_findings(vault_dir)
    if not findings:
        return None
    by_round = decay_tracker.group_by_round(findings)
    summaries = decay_tracker.summarize_rounds(by_round)
    if not summaries:
        return None
    latest = summaries[-1]
    streak = decay_tracker.clean_streak(summaries)
    real_findings = sum(
        1 for f in findings
        if f.severity not in ("informational",)
    )
    return SkillSummary(
        name=name,
        latest_round=latest.round,
        total_rounds=len(summaries),
        latest_structural=latest.structural,
        latest_cosmetic=latest.cosmetic,
        latest_minor=latest.minor,
        latest_clean=latest.clean,
        clean_streak=streak,
        ship_ready=streak >= zero_rounds_required,
        total_findings_all_time=real_findings,
    )


def render_skill_history(skill_name: str,
                         vault_dir: str,
                         zero_rounds_required: int = 2) -> str:
    """Full per-skill timeline: round-by-round table."""
    if not os.path.isdir(vault_dir):
        return "# .snes-fit history — {}\n\n_No vault found. Run `.snes-fit audit --skill {}` first._\n".format(
            skill_name, skill_name,
        )
    findings = decay_tracker.load_findings(vault_dir)
    if not findings:
        return "# .snes-fit history — {}\n\n_Vault exists but no findings recorded yet._\n".format(skill_name)

    by_round = decay_tracker.group_by_round(findings)
    summaries = decay_tracker.summarize_rounds(by_round)
    streak = decay_tracker.clean_streak(summaries)
    ship_ready = streak >= zero_rounds_required

    # Find timestamps per round (from round markers when available)
    round_timestamps: Dict[int, str] = {}
    for f in findings:
        if f.dimension == "_round_marker":
            round_timestamps[f.round] = f.timestamp_iso

    lines: List[str] = []
    lines.append("# .snes-fit history — {}".format(skill_name))
    lines.append("")
    lines.append("**Total rounds:** {}  |  **Clean streak:** {}  |  **Ship-ready:** {}".format(
        len(summaries), streak,
        "✅ YES" if ship_ready else "⏳ NO ({}/{})".format(streak, zero_rounds_required),
    ))
    lines.append("")
    lines.append("| 🟣 Round | 🟣 When | 🟣 Structural | 🟣 Cosmetic | 🟣 Minor | 🟣 Verdict |")
    lines.append("|---|---|---|---|---|---|")
    for s in summaries:
        ts = round_timestamps.get(s.round, "—")
        verdict = "🟢 CLEAN" if s.clean else "🔴 DIRTY"
        lines.append("| {} | {} | {} | {} | {} | {} |".format(
            s.round, ts, s.structural, s.cosmetic, s.minor, verdict,
        ))
    lines.append("")

    # Trailing detail: most recent non-marker findings
    real = [f for f in findings if f.dimension != "_round_marker"][-10:]
    if real:
        lines.append("## Most recent findings (last 10)")
        lines.append("")
        lines.append("| 🟣 Round | 🟣 Dimension | 🟣 Severity | 🟣 Message |")
        lines.append("|---|---|---|---|")
        for f in real:
            msg = f.message
            if len(msg) > 70:
                msg = msg[:67] + "..."
            lines.append("| {} | {} | {} | {} |".format(
                f.round, f.dimension, f.severity, msg,
            ))
    return "\n".join(lines) + "\n"


def render_fleet_history(vault_root: str,
                        zero_rounds_required: int = 2) -> str:
    """Fleet-wide trend table — one row per skill with its latest state."""
    if not os.path.isdir(vault_root):
        return "# .snes-fit fleet history\n\n_No vault directory yet._\n"
    skills_seen: List[Tuple[str, str]] = []
    for entry in sorted(os.listdir(vault_root)):
        full = os.path.join(vault_root, entry)
        if not os.path.isdir(full):
            continue
        skills_seen.append((entry, full))

    rows: List[SkillSummary] = []
    for name, path in skills_seen:
        s = summarize_skill(path, zero_rounds_required)
        if s is not None:
            rows.append(s)

    lines: List[str] = []
    lines.append("# .snes-fit fleet history")
    lines.append("")
    lines.append("**Skills audited (ever):** {}".format(len(rows)))
    ship_ready_count = sum(1 for r in rows if r.ship_ready)
    lines.append("**Ship-ready today:** {} / {}".format(ship_ready_count, len(rows)))
    lines.append("")

    if not rows:
        lines.append("_No audit history yet — run `.snes-fit audit --all` to populate._")
        return "\n".join(lines) + "\n"

    lines.append(
        "| 🟣 Skill | 🟣 Rounds | 🟣 Latest | 🟣 Struct | 🟣 Cosm | 🟣 Minor | 🟣 Streak | 🟣 Ship-ready |"
    )
    lines.append(
        "|---|---|---|---|---|---|---|---|"
    )
    rows.sort(key=lambda r: (-int(r.ship_ready), -r.clean_streak, r.name))
    for r in rows:
        ready = "✅" if r.ship_ready else "⏳ {}/{}".format(r.clean_streak, zero_rounds_required)
        verdict_icon = "🟢" if r.latest_clean else "🔴"
        lines.append("| {} | {} | {} R{} | {} | {} | {} | {} | {} |".format(
            r.name,
            r.total_rounds,
            verdict_icon, r.latest_round,
            r.latest_structural, r.latest_cosmetic, r.latest_minor,
            r.clean_streak, ready,
        ))
    lines.append("")
    lines.append("Legend: `Struct` = critical+major. `Cosm` = cosmetic. Rows sorted: ship-ready first, then by streak, then alphabetical.")
    return "\n".join(lines) + "\n"
