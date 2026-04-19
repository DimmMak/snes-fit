"""Dimension 02 — Scale.

Measures the skill's on-disk footprint and flags pathological growth.
Phase 1: file count and total bytes heuristics + per-file size cap.
"""
from __future__ import annotations

import os
import time
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding


MAX_FILES = 2000
MAX_TOTAL_BYTES = 50 * 1024 * 1024  # 50 MB
MAX_SINGLE_FILE_BYTES = 2 * 1024 * 1024  # 2 MB per file


class ScalePlugin(DimensionPlugin):
    name = "02_scale"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        findings: List[Finding] = []
        if target.file_count > MAX_FILES:
            findings.append(Finding(
                dimension=self.name,
                severity="minor",
                message="Skill has {} files (> {} threshold)".format(target.file_count, MAX_FILES),
                evidence=target.path,
            ))
        if target.total_bytes > MAX_TOTAL_BYTES:
            findings.append(Finding(
                dimension=self.name,
                severity="major",
                message="Skill is {:.1f} MB (> {} MB threshold)".format(
                    target.total_bytes / 1024 / 1024, MAX_TOTAL_BYTES // 1024 // 1024),
                evidence=target.path,
            ))
        # Walk once to find any single bloated file + timing benchmark
        t0 = time.perf_counter()
        biggest = ("", 0)
        for dirpath, dirnames, filenames in os.walk(target.path):
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                try:
                    sz = os.path.getsize(full)
                except OSError:
                    continue
                if sz > biggest[1]:
                    biggest = (full, sz)
                if sz > MAX_SINGLE_FILE_BYTES:
                    findings.append(Finding(
                        dimension=self.name,
                        severity="minor",
                        message="File > {} MB".format(MAX_SINGLE_FILE_BYTES // 1024 // 1024),
                        evidence="{} ({:.1f} MB)".format(full, sz / 1024 / 1024),
                    ))
        elapsed = time.perf_counter() - t0
        if elapsed > 5.0:
            findings.append(Finding(
                dimension=self.name,
                severity="minor",
                message="Tree walk took {:.2f}s (> 5s)".format(elapsed),
                evidence=target.path,
            ))
        return findings
