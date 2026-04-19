"""`.auto-test audit --all` — fleet sweep."""
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
    ap = argparse.ArgumentParser(description=".auto-test audit --all — fleet sweep")
    ap.add_argument("--fleet-root", default=DEFAULT_FLEET_ROOT)
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--skip", default="", help="comma-separated skills to skip")
    args = ap.parse_args(argv)

    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    skip.add("auto-test")  # do not recursively audit self by default

    skills = [s for s in tree_walker.discover_skills(args.fleet_root) if s.has_skill_md]
    sys.stdout.write("# .auto-test fleet sweep\n\n")
    sys.stdout.write("Discovered {} skills.\n\n".format(len(skills)))
    sys.stdout.write("| 🟣 Skill | 🟣 Score | 🟣 Grade | 🟣 Ship-ready |\n")
    sys.stdout.write("|---|---|---|---|\n")
    summary: List[dict] = []
    for s in skills:
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
