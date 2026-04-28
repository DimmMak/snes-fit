"""Dimension 07 — Structural.

Tree invariants:
  - SKILL.md present
  - standard subdir layout (scripts/, optional config/, prompts/, tests/)
  - no cross-skill Python imports (`from <sibling-skill>`)
  - tree depth <= 5
"""
from __future__ import annotations

import os
import re
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding


CANONICAL_SUBDIRS = {"scripts", "config", "prompts", "tests", "logs",
                     "dimensions", "evals", "vault", "reports", "data",
                     "audits", "notes", "skills", "examples", "schemas"}

MAX_DEPTH = 5


class StructuralPlugin(DimensionPlugin):
    name = "07_structural"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        findings: List[Finding] = []
        if not target.has_skill_md:
            findings.append(Finding(
                dimension=self.name, severity="critical",
                message="SKILL.md missing",
                evidence=target.path,
            ))
        # Subdir sanity — unknown top-level dirs are cosmetic
        for sub in target.subdirs:
            if sub not in CANONICAL_SUBDIRS and not sub.startswith("_"):
                findings.append(Finding(
                    dimension=self.name, severity="cosmetic",
                    message="Non-canonical top-level subdir: {}".format(sub),
                    evidence=os.path.join(target.path, sub),
                ))
        # Depth
        depth = _max_depth(target.path)
        if depth > MAX_DEPTH:
            findings.append(Finding(
                dimension=self.name, severity="minor",
                message="Tree depth {} > {}".format(depth, MAX_DEPTH),
                evidence=target.path,
            ))
        # Cross-skill imports
        fleet_root = os.path.dirname(target.path)
        sibling_names = set()
        try:
            for entry in os.listdir(fleet_root):
                full = os.path.join(fleet_root, entry)
                if os.path.isdir(full) and entry != target.name and not entry.startswith("."):
                    # python package-style identifier only
                    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", entry):
                        sibling_names.add(entry)
        except OSError:
            pass
        if sibling_names:
            import_rx = re.compile(
                r"^(?:from|import)\s+(" + "|".join(re.escape(s) for s in sibling_names) + r")\b",
                re.MULTILINE,
            )
            scripts_dir = os.path.join(target.path, "scripts")
            if os.path.isdir(scripts_dir):
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
                        for m in import_rx.finditer(text):
                            findings.append(Finding(
                                dimension=self.name, severity="major",
                                message="Cross-skill import: {}".format(m.group(1)),
                                evidence="{}:{}".format(full, text.count("\n", 0, m.start()) + 1),
                            ))
        return findings


def _max_depth(root: str) -> int:
    best = 0
    root_parts = os.path.normpath(root).count(os.sep)
    for dirpath, dirnames, _filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        depth = os.path.normpath(dirpath).count(os.sep) - root_parts
        if depth > best:
            best = depth
    return best
