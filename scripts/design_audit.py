"""`.snes-fit design-audit --skill <name>` — runs ONLY dimension 08."""
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


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=".snes-fit design-audit — dim 08 only")
    ap.add_argument("--skill", required=True)
    ap.add_argument("--round", type=int, default=None,
                    help="decay-tracker round number (default: auto-increment)")
    ap.add_argument("--fleet-root", default=DEFAULT_FLEET_ROOT)
    args = ap.parse_args(argv)
    res = run_audit(
        skill_name=args.skill,
        fleet_root=args.fleet_root,
        round_num=args.round,
        dimensions_filter=["08_design_audit"],
        write_vault=True,
        write_report=False,
    )
    sys.stdout.write(res["markdown"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
