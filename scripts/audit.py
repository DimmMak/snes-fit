"""`.auto-test audit --skill <name>` — run all enabled dims on one skill."""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import List, Optional

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from dimensions._plugin_base import DimensionResult  # noqa: E402
from scripts.lib import decay_tracker, regression_vault, report_renderer, scorecard, tree_walker  # noqa: E402
from scripts.lib.plugin_loader import discover_plugins  # noqa: E402


DEFAULT_FLEET_ROOT = os.path.expanduser("~/Desktop/CLAUDE CODE")


def _load_config() -> dict:
    cfg_path = os.path.join(_ROOT, "config", "dimensions.json")
    try:
        with open(cfg_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {"schema_version": "0.1", "dimensions": []}


def _load_thresholds() -> dict:
    p = os.path.join(_ROOT, "config", "thresholds.json")
    try:
        with open(p, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {"decay_zero_rounds": 2, "ship_score_threshold": 80}


def run_audit(skill_name: str,
              fleet_root: str = DEFAULT_FLEET_ROOT,
              round_num: Optional[int] = None,
              dimensions_filter: Optional[List[str]] = None,
              write_vault: bool = True,
              write_report: bool = True) -> dict:
    """Run one audit round.

    round_num=None means auto-increment (recommended). An explicit integer
    overrides and is only useful for tests or replaying a specific round.
    """
    cfg = _load_config()
    thresholds = _load_thresholds()
    dim_entries = cfg.get("dimensions", [])
    enabled_ids = [d["id"] for d in dim_entries if d.get("enabled", True)]
    weights = {d["id"]: float(d.get("weight", 1.0)) for d in dim_entries}
    requires_api = {d["id"]: bool(d.get("requires_api", False)) for d in dim_entries}
    if dimensions_filter:
        # Honor explicit user filter — allow opt-in to disabled dims.
        filter_set = set(dimensions_filter)
        known_ids = {d["id"] for d in dim_entries}
        enabled_ids = [i for i in dimensions_filter if i in known_ids]
        # fall back to configured-enabled filter if the explicit ones all matched
        if not enabled_ids:
            enabled_ids = [i for i in filter_set if i in known_ids]
    # API-required dims: if no API key and not mock mode, they'll emit UNKNOWN
    # findings rather than crash — handled inside each plugin.
    api_mode = _api_mode()
    skill = tree_walker.get_skill(fleet_root, skill_name)
    if skill is None:
        raise SystemExit("Skill not found: {} (under {})".format(skill_name, fleet_root))
    plugins = discover_plugins(enabled_ids=enabled_ids)

    # Auto-increment round if not explicitly set. Prevents the "every run is
    # round 1" bug where re-audits stacked markers under the same round id.
    vault_dir = os.path.join(_ROOT, "vault", skill_name)
    if round_num is None:
        existing = decay_tracker.load_findings(vault_dir)
        round_num = decay_tracker.next_round_id(
            decay_tracker.group_by_round(existing)
        )

    results: List[DimensionResult] = []
    for plugin in plugins:
        try:
            findings = plugin.probe(skill)
        except Exception as e:
            findings = []
            results.append(DimensionResult(
                dimension=plugin.name, score=0.0, findings=[], passed=False,
            ))
            sys.stderr.write("[warn] plugin {} raised: {}\n".format(plugin.name, e))
            continue
        score = plugin.score(findings)
        passed = score >= 0.8 and not any(f.severity == "critical" for f in findings)
        result = DimensionResult(
            dimension=plugin.name, score=score, findings=findings, passed=passed,
        )
        results.append(result)

    # Aggregate first — need total_score for the round marker
    total_score = scorecard.calculate_score(results, weights=weights)
    letter = scorecard.grade(total_score)

    # Write findings to vault
    if write_vault:
        for r in results:
            for f in r.findings:
                regression_vault.append_finding(vault_dir, {
                    "schema_version": "0.1",
                    "timestamp_iso": _now_iso(),
                    "round": round_num,
                    "dimension": f.dimension,
                    "severity": f.severity,
                    "message": f.message,
                    "evidence": f.evidence,
                })
        # Always write a round-complete marker so zero-finding rounds are
        # visible to the decay tracker. Without this, a clean round leaves
        # no trace in findings.jsonl and is_ship_ready can't count it.
        # severity='informational' is ignored by _is_zero_round's structural+cosmetic counts.
        round_finding_count = sum(len(r.findings) for r in results)
        regression_vault.append_finding(vault_dir, {
            "schema_version": "0.1",
            "timestamp_iso": _now_iso(),
            "round": round_num,
            "dimension": "_round_marker",
            "severity": "informational",
            "message": "round {} complete ({} findings, score={})".format(
                round_num, round_finding_count, total_score,
            ),
            "evidence": "auto-generated by audit.py",
        })

    # Decay read-back
    found = decay_tracker.load_findings(vault_dir)
    by_round = decay_tracker.group_by_round(found)
    summaries = decay_tracker.summarize_rounds(by_round)
    streak = decay_tracker.clean_streak(summaries)
    zero_rounds_required = int(thresholds.get("decay_zero_rounds", 2))
    ship_ready = (
        streak >= zero_rounds_required
        and total_score >= int(thresholds.get("ship_score_threshold", 80))
    )

    # Render report
    md = report_renderer.render_scorecard(
        skill=skill_name, results=results,
        round_summaries=summaries, clean_streak=streak,
        zero_rounds_required=zero_rounds_required,
        score=total_score, grade=letter,
        ship_ready=ship_ready,
    )
    if write_report:
        reports_dir = os.path.join(_ROOT, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        rpath = os.path.join(reports_dir, "{}-{}.md".format(
            datetime.now(timezone.utc).strftime("%Y-%m-%d"), skill_name,
        ))
        with open(rpath, "w", encoding="utf-8") as fh:
            fh.write(md)

    # Cost estimate log (best-effort): note API dims touched this run.
    touched_api_dims = [p.name for p in plugins if requires_api.get(p.name)]
    if touched_api_dims:
        sys.stderr.write(
            "[auto-test] API-required dims ran in mode={}: {}\n".format(
                api_mode, ", ".join(touched_api_dims),
            )
        )

    return {
        "skill": skill_name,
        "score": total_score,
        "grade": letter,
        "ship_ready": ship_ready,
        "results": results,
        "markdown": md,
        "api_mode": api_mode,
        "api_dims_ran": touched_api_dims,
    }


def _api_mode() -> str:
    if os.getenv("AUTO_TEST_MOCK") == "1":
        return "mock"
    if os.getenv("ANTHROPIC_API_KEY"):
        return "live"
    return "no-api"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=".auto-test audit — run all enabled dims on one skill")
    ap.add_argument("--skill", required=True, help="skill name (directory under fleet root)")
    ap.add_argument("--round", type=int, default=None,
                    help="decay-tracker round number (default: auto-increment)")
    ap.add_argument("--dimensions", default="", help="comma-separated dimension id filter")
    ap.add_argument("--fleet-root", default=DEFAULT_FLEET_ROOT)
    ap.add_argument("--no-vault", action="store_true", help="skip writing to vault")
    ap.add_argument("--no-report", action="store_true", help="skip writing report file")
    args = ap.parse_args(argv)
    dim_filter = [s.strip() for s in args.dimensions.split(",") if s.strip()] or None
    out = run_audit(
        skill_name=args.skill,
        fleet_root=args.fleet_root,
        round_num=args.round,
        dimensions_filter=dim_filter,
        write_vault=not args.no_vault,
        write_report=not args.no_report,
    )
    sys.stdout.write(out["markdown"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
