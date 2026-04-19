"""Dimension 03 — Composition.

Reads the skill's SKILL.md frontmatter, extracts `composable_with`,
verifies each listed sibling skill actually exists on disk.
"""
from __future__ import annotations

import os
import re
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding


FRONTMATTER_RX = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
COMPOSABLE_RX = re.compile(r"composable_with\s*:\s*\n((?:\s*-\s*.+\n?)+)", re.MULTILINE)
ITEM_RX = re.compile(r"^\s*-\s*[\"']?([^\"'\n]+?)[\"']?\s*$", re.MULTILINE)


class CompositionPlugin(DimensionPlugin):
    name = "03_composition"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        findings: List[Finding] = []
        skill_md = os.path.join(target.path, "SKILL.md")
        if not os.path.isfile(skill_md):
            return findings  # structural dim handles missing SKILL.md
        try:
            with open(skill_md, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            return findings
        fm = FRONTMATTER_RX.match(text)
        if not fm:
            findings.append(Finding(
                dimension=self.name, severity="minor",
                message="SKILL.md has no YAML frontmatter",
                evidence=skill_md,
            ))
            return findings
        fm_body = fm.group(1)
        comp_match = COMPOSABLE_RX.search(fm_body)
        if not comp_match:
            findings.append(Finding(
                dimension=self.name, severity="cosmetic",
                message="No composable_with list declared",
                evidence=skill_md,
            ))
            return findings
        block = comp_match.group(1)
        listed = [m.group(1).strip() for m in ITEM_RX.finditer(block)]
        # Fleet root = parent of this skill's path
        fleet_root = os.path.dirname(target.path)
        for sibling in listed:
            sibling_clean = sibling.strip("\"' ")
            # allow "." prefix (user-facing) and bare names
            candidate = sibling_clean.lstrip(".")
            sibling_path = os.path.join(fleet_root, candidate)
            if not os.path.isdir(sibling_path):
                findings.append(Finding(
                    dimension=self.name, severity="major",
                    message="composable_with references missing skill: {!r}".format(sibling_clean),
                    evidence=sibling_path,
                ))
        return findings
