"""`.snes-fit audit --all` — fleet sweep."""
from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.audit import run_audit, DEFAULT_FLEET_ROOT  # noqa: E402
from scripts.lib import tree_walker  # noqa: E402


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=".snes-fit audit --all — fleet sweep")
    ap.add_argument("--fleet-root", default=DEFAULT_FLEET_ROOT)
    ap.add_argument("--round", type=int, default=None,
                    help="decay-tracker round number (default: auto-increment per skill)")
    ap.add_argument("--skip", default="", help="comma-separated skills to skip")
    args = ap.parse_args(argv)

    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    # NOTE (2026-04-28 — forensic CRIT #2 followup): the previous version of
    # this file added `skip.add("snes-fit")` here, hard-coding a self-skip in
    # the fleet sweep. That contradicted the dim 00_self design (snes-fit
    # auditing itself) and re-introduced the audit-the-auditor blind spot.
    # snes-fit is now included in the sweep by default. To skip it explicitly,
    # pass `--skip snes-fit`.

    skills = [s for s in tree_walker.discover_skills(args.fleet_root) if s.has_skill_md]
    sys.stdout.write("# .snes-fit fleet sweep\n\n")
    sys.stdout.write("Discovered {} skills.\n\n".format(len(skills)))
    sys.stdout.write("| 🟣 Skill | 🟣 Score | 🟣 Grade | 🟣 Ship-ready |\n")
    sys.stdout.write("|---|---|---|---|\n")
    summary: List[dict] = []

    # Run snes-fit FIRST so a self-audit failure can abort the sweep before
    # we audit anything else. If the auditor doesn't pass its own bar, every
    # downstream grade is suspect.
    skills_sorted = sorted(skills, key=lambda s: (0 if s.name == "snes-fit" else 1, s.name))

    for s in skills_sorted:
        if s.name in skip:
            continue
        try:
            res = run_audit(
                skill_name=s.name,
                fleet_root=args.fleet_root,
                round_num=args.round,
                write_vault=True,
                write_report=True,
            )
            sys.stdout.write("| {} | {} | {} | {} |\n".format(
                s.name, res["score"], res["grade"],
                "YES" if res["ship_ready"] else "NO",
            ))
            summary.append(res)
        except SystemExit:
            continue
        except Exception as e:
            sys.stderr.write("[error] {}: {}\n".format(s.name, e))
            sys.stdout.write("| {} | — | — | ERROR |\n".format(s.name))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
