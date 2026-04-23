"""`.snes-fit history <skill>` or `.snes-fit history --all`.

Renders audit history as markdown — timeline for one skill or fleet-wide
summary. Read-only; never mutates vault data.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List, Optional

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.lib import history_renderer  # noqa: E402


def _load_thresholds() -> dict:
    p = os.path.join(_ROOT, "config", "thresholds.json")
    try:
        with open(p, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {"decay_zero_rounds": 2}


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description=".snes-fit history — per-skill or fleet-wide audit timeline"
    )
    ap.add_argument("--skill", default=None, help="skill name (omit with --all)")
    ap.add_argument("--all", action="store_true", help="fleet-wide summary")
    args = ap.parse_args(argv)

    thresholds = _load_thresholds()
    zero_rounds = int(thresholds.get("decay_zero_rounds", 2))

    vault_root = os.path.join(_ROOT, "vault")

    if args.all or not args.skill:
        sys.stdout.write(
            history_renderer.render_fleet_history(vault_root, zero_rounds)
        )
        return 0

    vault_dir = os.path.join(vault_root, args.skill)
    sys.stdout.write(
        history_renderer.render_skill_history(args.skill, vault_dir, zero_rounds)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
