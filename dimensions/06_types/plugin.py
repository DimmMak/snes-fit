"""Dimension 06 — Types.

AST-based type-hint coverage. Flags functions that are missing
parameter or return-type annotations. No mypy yet — phase 2.
"""
from __future__ import annotations

import ast
import os
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding


COVERAGE_MIN = 0.5  # 50% of functions should be annotated


class TypesPlugin(DimensionPlugin):
    name = "06_types"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        findings: List[Finding] = []
        scripts_dir = os.path.join(target.path, "scripts")
        if not os.path.isdir(scripts_dir):
            return findings
        total = 0
        annotated = 0
        for dirpath, _dirnames, filenames in os.walk(scripts_dir):
            for fn in filenames:
                if not fn.endswith(".py"):
                    continue
                full = os.path.join(dirpath, fn)
                try:
                    with open(full, "r", encoding="utf-8", errors="replace") as fh:
                        src = fh.read()
                except OSError:
                    continue
                try:
                    tree = ast.parse(src, filename=full)
                except SyntaxError as e:
                    findings.append(Finding(
                        dimension=self.name, severity="major",
                        message="SyntaxError: {}".format(e.msg),
                        evidence="{}:{}".format(full, e.lineno or 0),
                    ))
                    continue
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if node.name.startswith("_") and node.name != "__init__":
                            continue
                        total += 1
                        has_return = node.returns is not None
                        params = [a for a in node.args.args if a.arg != "self" and a.arg != "cls"]
                        all_params_annotated = all(a.annotation is not None for a in params) if params else True
                        if has_return and all_params_annotated:
                            annotated += 1
        if total == 0:
            return findings
        coverage = annotated / total
        if coverage < COVERAGE_MIN:
            findings.append(Finding(
                dimension=self.name, severity="minor",
                message="Type-hint coverage {:.0%} (< {:.0%} threshold)".format(coverage, COVERAGE_MIN),
                evidence="{}/scripts/ — {}/{} functions annotated".format(target.path, annotated, total),
            ))
        return findings
