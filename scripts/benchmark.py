"""`.auto-test benchmark --skill <name>` — rolling baseline + delta."""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from typing import List, Optional

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.audit import run_audit, DEFAULT_FLEET_ROOT  # noqa: E402
from scripts.lib import regression_vault  # noqa: E402


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=".auto-test benchmark")
    ap.add_argument("--skill", required=True)
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--fleet-root", default=DEFAULT_FLEET_ROOT)
    args = ap.parse_args(argv)

    res = run_audit(
        skill_name=args.skill,
        fleet_root=args.fleet_root,
        round_num=args.round,
        write_vault=True,
        write_report=False,
    )

    vault_dir = os.path.join(_ROOT, "vault", args.skill)
    prev = list(regression_vault.iter_benchmark(vault_dir))
    per_dim = {r.dimension: r.score for r in res["results"]}
    record = {
        "schema_version": "0.1",
        "timestamp_iso": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "run_id": "run_{}".format(len(prev) + 1),
        "overall_score": res["score"],
        "grade": res["grade"],
        "per_dim": per_dim,
    }
    regression_vault.append_benchmark(vault_dir, record)

    sys.stdout.write("# Benchmark — {}\n\n".format(args.skill))
    sys.stdout.write("Score: {}  |  Grade: {}\n\n".format(res["score"], res["grade"]))
    if prev:
        last = prev[-1]
        last_score = int(last.get("overall_score", 0))
        delta = res["score"] - last_score
        sys.stdout.write("Previous: {}  |  Delta: {:+d}\n\n".format(last_score, delta))
    else:
        sys.stdout.write("No prior benchmark recorded — this is baseline.\n\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
