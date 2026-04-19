"""`.auto-test create --skill <name>` — scaffold Anthropic-compatible evals.json."""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List, Optional

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))


TEMPLATE = {
    "schema_version": "0.1",
    "skill_name": "<skill>",
    "evals": [
        {
            "id": "eval_001",
            "prompt": "Describe a typical invocation of this skill.",
            "expected_output": "<substring the output must contain>",
            "files": [],
            "expectations": ["exit_code=0"],
        },
        {
            "id": "eval_002",
            "prompt": "Show the skill's status command output.",
            "expected_output": "status",
            "files": [],
            "expectations": ["contains:status"],
        },
        {
            "id": "eval_003",
            "prompt": "Exercise a failure path (bad input).",
            "expected_output": "error",
            "files": [],
            "expectations": ["exit_code!=0"],
        },
    ],
}


def scaffold(skill_name: str, force: bool = False) -> str:
    evals_dir = os.path.join(_ROOT, "evals", skill_name)
    os.makedirs(evals_dir, exist_ok=True)
    target = os.path.join(evals_dir, "evals.json")
    if os.path.exists(target) and not force:
        raise SystemExit(
            "evals.json already exists at {} (pass --force to overwrite)".format(target)
        )
    payload = dict(TEMPLATE)
    payload["skill_name"] = skill_name
    with open(target, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
    return target


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=".auto-test create — scaffold eval suite")
    ap.add_argument("--skill", required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    path = scaffold(args.skill, force=args.force)
    sys.stdout.write("Scaffolded {}\n".format(path))
    sys.stdout.write("Edit the file to add real evals, then run:\n")
    sys.stdout.write("  python3 -m scripts.audit --skill {}\n".format(args.skill))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
