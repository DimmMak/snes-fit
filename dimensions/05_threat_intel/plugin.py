"""Dimension 05 — Threat intel (i18n / injection surface).

Scans data + docs for:
  - CRLF injection markers (\r\n in unexpected places)
  - BOM at the start of text files (parser breakage)
  - Homograph / confusable characters (Cyrillic 'а' vs Latin 'a' etc.)
"""
from __future__ import annotations

import os
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding


# A compact homograph set — Latin letter : confusable Cyrillic codepoint.
CONFUSABLES = {
    "a": "\u0430", "c": "\u0441", "e": "\u0435", "o": "\u043e",
    "p": "\u0440", "x": "\u0445", "y": "\u0443",
    "A": "\u0410", "B": "\u0412", "E": "\u0415", "H": "\u041d",
    "K": "\u041a", "M": "\u041c", "O": "\u041e", "P": "\u0420",
    "T": "\u0422", "X": "\u0425",
}
CONFUSABLE_SET = set(CONFUSABLES.values())

TEXT_EXTS = (".md", ".txt", ".json", ".jsonl", ".py", ".yaml", ".yml", ".sh")


class ThreatIntelPlugin(DimensionPlugin):
    name = "05_threat_intel"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        findings: List[Finding] = []
        for dirpath, dirnames, filenames in os.walk(target.path):
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
            for fn in filenames:
                if not fn.endswith(TEXT_EXTS):
                    continue
                full = os.path.join(dirpath, fn)
                try:
                    with open(full, "rb") as fh:
                        raw = fh.read()
                except OSError:
                    continue
                # BOM check
                if raw.startswith(b"\xef\xbb\xbf"):
                    findings.append(Finding(
                        dimension=self.name, severity="minor",
                        message="UTF-8 BOM at file start (breaks naive parsers)",
                        evidence=full,
                    ))
                # Skip this plugin file itself when scanning for confusables
                # (our CONFUSABLES dict intentionally contains them).
                is_self = full.endswith(os.path.join("05_threat_intel", "plugin.py"))
                # CRLF check (on files that aren't windows batch/powershell)
                if b"\r\n" in raw and not fn.endswith((".bat", ".ps1", ".cmd")):
                    findings.append(Finding(
                        dimension=self.name, severity="cosmetic",
                        message="CRLF line endings (expected LF)",
                        evidence=full,
                    ))
                # Homograph scan
                if is_self:
                    continue
                try:
                    text = raw.decode("utf-8", errors="replace")
                except Exception:
                    continue
                bad = 0
                for ch in text:
                    if ch in CONFUSABLE_SET:
                        bad += 1
                        if bad >= 3:  # noise threshold
                            break
                if bad >= 3:
                    findings.append(Finding(
                        dimension=self.name, severity="major",
                        message="Contains homograph / confusable characters",
                        evidence=full,
                    ))
        return findings
