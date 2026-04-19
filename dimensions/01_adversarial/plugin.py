"""Dimension 01 — Adversarial.

Phase 1 (stdlib-only): static check that every .py file under scripts/
handles hostile input at least nominally. Heuristic: each top-level
function should either have a try/except, argparse-style validation,
or a type hint suggesting Optional. Flags files that are obviously
fragile (e.g. unguarded `sys.argv[1]` indexing).
"""
from __future__ import annotations

import os
import re
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding


HOSTILE_PATTERNS = [
    # unguarded sys.argv indexing (IndexError waiting to happen)
    (re.compile(r"sys\.argv\[\s*[1-9]"), "unguarded sys.argv indexing", "minor"),
    # bare except eats adversarial info
    (re.compile(r"^\s*except\s*:\s*$", re.MULTILINE), "bare except clause", "minor"),
    # eval/exec on untrusted input
    (re.compile(r"\beval\s*\("), "use of eval()", "major"),
    (re.compile(r"\bexec\s*\("), "use of exec()", "major"),
]


class AdversarialPlugin(DimensionPlugin):
    name = "01_adversarial"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        """`target` is a SkillInfo. Scan scripts/ for fragile patterns."""
        findings: List[Finding] = []
        scripts_dir = os.path.join(target.path, "scripts")
        if not os.path.isdir(scripts_dir):
            return findings
        for dirpath, _dirnames, filenames in os.walk(scripts_dir):
            for fn in filenames:
                if not fn.endswith(".py"):
                    continue
                full = os.path.join(dirpath, fn)
                try:
                    with open(full, "r", encoding="utf-8", errors="replace") as fh:
                        text = fh.read()
                except OSError:
                    continue
                for rx, msg, sev in HOSTILE_PATTERNS:
                    for m in rx.finditer(text):
                        findings.append(Finding(
                            dimension=self.name,
                            severity=sev,
                            message=msg,
                            evidence="{}:{}".format(full, _line_of(text, m.start())),
                        ))
        return findings


def _line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1
