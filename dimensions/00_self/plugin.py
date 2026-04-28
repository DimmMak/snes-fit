"""Dimension 00 — Self.

Audit-the-auditor: validates snes-fit's own conformance to SPEC.md.
Closes the self-reference paradox identified in forensic CRIT #2 (2026-04-28).

Runs ONLY when target.name == "snes-fit". For all other skills the probe
returns no findings — dim 07 (structural) and dim 08 (design_audit) handle
non-self skills. The unique value-add here is asking: "does snes-fit clear
its own bar?" Without this dimension, the auditor is unaudited.
"""
from __future__ import annotations

import os
import re
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding


REQUIRED_BODY_SECTIONS = (
    "## Purpose",
    "## When to trigger",
    "## When NOT to trigger",
    "## Anti-patterns",
    "## Exit conditions",
)

REQUIRED_FILES = (
    "SKILL.md",
    "ARCHITECTURE.md",
    "SCHEMA.md",
    "CHANGELOG.md",
)


class SelfAuditPlugin(DimensionPlugin):
    name = "00_self"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        # Only audits snes-fit itself.
        if getattr(target, "name", "") != "snes-fit":
            return []

        findings: List[Finding] = []

        for fname in REQUIRED_FILES:
            full = os.path.join(target.path, fname)
            if not os.path.isfile(full):
                findings.append(Finding(
                    dimension=self.name,
                    severity="critical",
                    message="Required file missing per SPEC.md: {}".format(fname),
                    evidence=full,
                ))

        skill_md_path = os.path.join(target.path, "SKILL.md")
        try:
            with open(skill_md_path, "r", encoding="utf-8") as fh:
                skill_md_text = fh.read()
        except OSError:
            skill_md_text = ""

        non_goals_file = os.path.join(target.path, "NON_GOALS.md")
        has_non_goals = (
            os.path.isfile(non_goals_file)
            or re.search(r"^## Non-goals", skill_md_text, re.MULTILINE | re.IGNORECASE)
        )
        if not has_non_goals:
            findings.append(Finding(
                dimension=self.name,
                severity="minor",
                message="Neither NON_GOALS.md nor '## Non-goals' section in SKILL.md",
                evidence=target.path,
            ))

        for section in REQUIRED_BODY_SECTIONS:
            if section.lower() not in skill_md_text.lower():
                findings.append(Finding(
                    dimension=self.name,
                    severity="critical",
                    message="Required body section missing per SPEC.md:55-64: {}".format(section),
                    evidence=skill_md_path,
                ))

        fm_match = re.match(r"^---\n(.*?)\n---", skill_md_text, re.DOTALL)
        if not fm_match:
            findings.append(Finding(
                dimension=self.name,
                severity="critical",
                message="No YAML frontmatter at top of SKILL.md",
                evidence=skill_md_path,
            ))
        else:
            frontmatter = fm_match.group(1)
            if not re.search(r"^name:\s*", frontmatter, re.MULTILINE):
                findings.append(Finding(
                    dimension=self.name,
                    severity="critical",
                    message="Frontmatter missing required field: name",
                    evidence=skill_md_path,
                ))
            if not re.search(r"^description:\s*", frontmatter, re.MULTILINE):
                findings.append(Finding(
                    dimension=self.name,
                    severity="critical",
                    message="Frontmatter missing required field: description",
                    evidence=skill_md_path,
                ))
            not_for_count = len(re.findall(r"NOT for:", frontmatter))
            if not_for_count < 2:
                findings.append(Finding(
                    dimension=self.name,
                    severity="major",
                    message="Description must include NOT for: clauses naming 2+ sibling skills (found {})".format(not_for_count),
                    evidence=skill_md_path,
                ))

        return findings
