"""Dimension 08 — Design audit.

Checks the skill's *design documentation* is present and well-versioned:
  - ARCHITECTURE.md present
  - SCHEMA.md present
  - NON_GOALS.md present OR SKILL.md contains a "Non-goals" section
  - CHANGELOG.md present
  - schema_version field appears in any JSON / JSONL config or log file
"""
from __future__ import annotations

import json
import os
import re
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding


NON_GOALS_HEADER_RX = re.compile(r"^#+\s*non[- ]?goals?\b", re.IGNORECASE | re.MULTILINE)


class DesignAuditPlugin(DimensionPlugin):
    name = "08_design_audit"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        findings: List[Finding] = []
        req_docs = [
            ("ARCHITECTURE.md", "major"),
            ("SCHEMA.md", "major"),
            ("CHANGELOG.md", "minor"),
        ]
        for fn, sev in req_docs:
            p = os.path.join(target.path, fn)
            if not os.path.isfile(p):
                findings.append(Finding(
                    dimension=self.name, severity=sev,
                    message="Missing design doc: {}".format(fn),
                    evidence=p,
                ))
        # Non-goals: dedicated file OR section in SKILL.md
        non_goals_ok = os.path.isfile(os.path.join(target.path, "NON_GOALS.md"))
        if not non_goals_ok:
            skill_md = os.path.join(target.path, "SKILL.md")
            if os.path.isfile(skill_md):
                try:
                    with open(skill_md, "r", encoding="utf-8", errors="replace") as fh:
                        if NON_GOALS_HEADER_RX.search(fh.read()):
                            non_goals_ok = True
                except OSError:
                    pass
        if not non_goals_ok:
            findings.append(Finding(
                dimension=self.name, severity="minor",
                message="No NON_GOALS.md and no 'Non-goals' section in SKILL.md",
                evidence=target.path,
            ))
        # schema_version appears in at least one JSON/JSONL under config/ or logs/
        if not self._has_schema_version(target.path):
            findings.append(Finding(
                dimension=self.name, severity="minor",
                message="No schema_version field found in any config/*.json or logs/*.jsonl",
                evidence=target.path,
            ))
        return findings

    @staticmethod
    def _has_schema_version(skill_path: str) -> bool:
        scan_dirs = ["config", "logs", "vault", "data"]
        for sub in scan_dirs:
            d = os.path.join(skill_path, sub)
            if not os.path.isdir(d):
                continue
            for dirpath, _dirnames, filenames in os.walk(d):
                for fn in filenames:
                    if fn.endswith(".json"):
                        try:
                            with open(os.path.join(dirpath, fn), "r", encoding="utf-8") as fh:
                                data = json.load(fh)
                            if isinstance(data, dict) and "schema_version" in data:
                                return True
                        except (OSError, json.JSONDecodeError):
                            continue
                    elif fn.endswith(".jsonl"):
                        try:
                            with open(os.path.join(dirpath, fn), "r", encoding="utf-8") as fh:
                                for line in fh:
                                    line = line.strip()
                                    if not line:
                                        continue
                                    try:
                                        d2 = json.loads(line)
                                    except json.JSONDecodeError:
                                        continue
                                    if isinstance(d2, dict) and "schema_version" in d2:
                                        return True
                                    break  # only first line matters
                        except OSError:
                            continue
        return False
