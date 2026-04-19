"""Dimension 04 — Security.

Scans the skill for:
  - path traversal patterns (../ in file ops)
  - ReDoS heuristic (catastrophic backtracking: nested quantifiers)
  - hardcoded secret patterns (API keys, tokens, passwords)

Baseline: OWASP LLM Top 10 + common Python CWEs.
"""
from __future__ import annotations

import os
import re
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding


# Heuristic secret detectors — err toward recall; false positives are acceptable.
SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key", "critical"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI/Anthropic-style API key", "critical"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub personal access token", "critical"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token", "critical"),
    (re.compile(r"(?i)password\s*[:=]\s*[\"'][^\"']{6,}[\"']"), "hardcoded password literal", "major"),
    (re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"), "private key material", "critical"),
]

# ReDoS heuristic: nested quantifiers inside a capture group.
REDOS_RX = re.compile(r"\((?:[^()]*[+*]){2,}[^()]*\)[+*]")

PATH_TRAVERSAL_RX = re.compile(r"open\s*\(\s*[^)]*\.\./")


class SecurityPlugin(DimensionPlugin):
    name = "04_security"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        findings: List[Finding] = []
        for dirpath, dirnames, filenames in os.walk(target.path):
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
            for fn in filenames:
                if fn.endswith((".pyc", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip")):
                    continue
                full = os.path.join(dirpath, fn)
                try:
                    with open(full, "r", encoding="utf-8", errors="replace") as fh:
                        text = fh.read()
                except OSError:
                    continue
                # Skip scanning our own pattern list (false self-match).
                if full.endswith(os.path.join("04_security", "plugin.py")):
                    continue
                for rx, label, sev in SECRET_PATTERNS:
                    for m in rx.finditer(text):
                        findings.append(Finding(
                            dimension=self.name, severity=sev,
                            message="Possible secret: {}".format(label),
                            evidence="{}:{}".format(full, _line_of(text, m.start())),
                        ))
                for m in PATH_TRAVERSAL_RX.finditer(text):
                    findings.append(Finding(
                        dimension=self.name, severity="major",
                        message="Possible path traversal in open()",
                        evidence="{}:{}".format(full, _line_of(text, m.start())),
                    ))
                if fn.endswith(".py"):
                    for m in REDOS_RX.finditer(text):
                        findings.append(Finding(
                            dimension=self.name, severity="minor",
                            message="Possible ReDoS (nested quantifiers)",
                            evidence="{}:{}".format(full, _line_of(text, m.start())),
                        ))
        return findings


def _line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1
