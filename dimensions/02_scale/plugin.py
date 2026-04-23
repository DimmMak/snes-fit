"""Dimension 02 — Scale.

Measures the skill's on-disk footprint and flags pathological growth.
Phase 1: file count and total bytes heuristics + per-file size cap.

Files under data/cache/ are exempt from size caps per SNES-fit SPEC v0.2
(data caches are legitimate for API-rate-limited skills like filings-desk,
price-desk history, earnings-desk, etc.).
"""
from __future__ import annotations

import os
import time
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding
from scripts.lib.tree_walker import prune_excluded_dirs, is_excluded_file


MAX_FILES = 2000
MAX_TOTAL_BYTES = 50 * 1024 * 1024  # 50 MB
MAX_SINGLE_FILE_BYTES = 2 * 1024 * 1024  # 2 MB per file


def _is_cache_path(full_path: str, skill_root: str) -> bool:
    """True if path is under data/cache/ relative to skill root.

    Per SNES-fit SPEC v0.2: data/cache/** is exempt from size caps.
    """
    try:
        rel = os.path.relpath(full_path, skill_root)
    except ValueError:
        return False
    parts = rel.split(os.sep)
    return len(parts) >= 2 and parts[0] == "data" and parts[1] == "cache"


class ScalePlugin(DimensionPlugin):
    name = "02_scale"
    version = "0.2.0"  # cache exemption
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        findings: List[Finding] = []
        t0 = time.perf_counter()

        # Recompute sizes excluding data/cache/ per SPEC exemption.
        non_cache_files = 0
        non_cache_bytes = 0
        for dirpath, dirnames, filenames in os.walk(target.path):
            prune_excluded_dirs(dirnames)
            for fn in filenames:
                if is_excluded_file(fn):
                    continue
                full = os.path.join(dirpath, fn)
                try:
                    sz = os.path.getsize(full)
                except OSError:
                    continue
                if _is_cache_path(full, target.path):
                    continue  # exempt per SPEC
                non_cache_files += 1
                non_cache_bytes += sz
                if sz > MAX_SINGLE_FILE_BYTES:
                    findings.append(Finding(
                        dimension=self.name,
                        severity="minor",
                        message="File > {} MB".format(MAX_SINGLE_FILE_BYTES // 1024 // 1024),
                        evidence="{} ({:.1f} MB)".format(full, sz / 1024 / 1024),
                    ))

        if non_cache_files > MAX_FILES:
            findings.append(Finding(
                dimension=self.name,
                severity="minor",
                message="Skill has {} non-cache files (> {} threshold)".format(non_cache_files, MAX_FILES),
                evidence=target.path,
            ))
        if non_cache_bytes > MAX_TOTAL_BYTES:
            findings.append(Finding(
                dimension=self.name,
                severity="major",
                message="Skill is {:.1f} MB excluding data/cache/ (> {} MB threshold)".format(
                    non_cache_bytes / 1024 / 1024, MAX_TOTAL_BYTES // 1024 // 1024),
                evidence=target.path,
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
