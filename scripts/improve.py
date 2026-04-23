"""`.snes-fit improve --skill <name>` — phase-1 stub.

Phase 2 will call the LLM judge on each finding and emit proposed patches.
For now we summarize the latest vault findings so the human can act.
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from typing import List, Optional

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.lib import regression_vault  # noqa: E402


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=".snes-fit improve — phase-1 stub")
    ap.add_argument("--skill", required=True)
    args = ap.parse_args(argv)
    vault_dir = os.path.join(_ROOT, "vault", args.skill)
    findings = list(regression_vault.iter_findings(vault_dir))
    sys.stdout.write("# Improve mode (phase 1 stub)\n\n")
    sys.stdout.write(
        "LLM-backed suggestion engine is reserved for phase 2 "
        "(executor=claude-sonnet-4-7, judge=claude-haiku-4-5).\n\n"
    )
    sys.stdout.write("## Current vault snapshot\n\n")
    sys.stdout.write("Total findings: {}\n\n".format(len(findings)))
    if findings:
        by_sev = Counter(f.get("severity", "minor") for f in findings)
        by_dim = Counter(f.get("dimension", "unknown") for f in findings)
        sys.stdout.write("| 🟣 Severity | 🟣 Count |\n|---|---|\n")
        for sev in ("critical", "major", "minor", "cosmetic"):
            sys.stdout.write("| {} | {} |\n".format(sev, by_sev.get(sev, 0)))
        sys.stdout.write("\n| 🟣 Dimension | 🟣 Count |\n|---|---|\n")
        for dim, ct in sorted(by_dim.items()):
            sys.stdout.write("| {} | {} |\n".format(dim, ct))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
