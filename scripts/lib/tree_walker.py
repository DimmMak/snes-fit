"""Fleet discovery + structural introspection.

Walks a fleet root (default `~/Desktop/CLAUDE CODE/`) and returns one
`SkillInfo` per directory that looks like a skill (contains SKILL.md).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional


CANONICAL_SUBDIRS = ("scripts", "config", "prompts", "tests", "dimensions", "logs")


@dataclass
class SkillInfo:
    name: str
    path: str
    has_skill_md: bool
    subdirs: List[str] = field(default_factory=list)
    file_count: int = 0
    total_bytes: int = 0


@dataclass
class StructuralIssue:
    kind: str      # e.g. "missing_skill_md", "unknown_subdir", "deep_tree"
    message: str
    evidence: str


def discover_skills(root: str) -> List[SkillInfo]:
    """Return one SkillInfo per direct child of `root` that contains SKILL.md."""
    results: List[SkillInfo] = []
    if not os.path.isdir(root):
        return results
    for entry in sorted(os.listdir(root)):
        full = os.path.join(root, entry)
        if not os.path.isdir(full):
            continue
        if entry.startswith(".") or entry.startswith("_"):
            continue
        results.append(_build_skill_info(entry, full))
    return results


def _build_skill_info(name: str, path: str) -> SkillInfo:
    has_skill_md = os.path.isfile(os.path.join(path, "SKILL.md"))
    subdirs: List[str] = []
    file_count = 0
    total_bytes = 0
    try:
        for entry in os.listdir(path):
            if os.path.isdir(os.path.join(path, entry)) and not entry.startswith("."):
                subdirs.append(entry)
    except OSError:
        pass
    for dirpath, dirnames, filenames in os.walk(path):
        # prune hidden dirs
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        for fn in filenames:
            file_count += 1
            try:
                total_bytes += os.path.getsize(os.path.join(dirpath, fn))
            except OSError:
                pass
    return SkillInfo(
        name=name,
        path=path,
        has_skill_md=has_skill_md,
        subdirs=sorted(subdirs),
        file_count=file_count,
        total_bytes=total_bytes,
    )


def get_skill(root: str, name: str) -> Optional[SkillInfo]:
    """Return a single SkillInfo by name, or None if not found."""
    path = os.path.join(root, name)
    if not os.path.isdir(path):
        return None
    return _build_skill_info(name, path)


def validate_tree(skill: SkillInfo, max_depth: int = 5) -> List[StructuralIssue]:
    """Check canonical subdir layout + tree depth."""
    issues: List[StructuralIssue] = []
    if not skill.has_skill_md:
        issues.append(StructuralIssue("missing_skill_md", "SKILL.md not found", skill.path))
    # depth check
    depth = _max_depth(skill.path)
    if depth > max_depth:
        issues.append(
            StructuralIssue("deep_tree", "tree depth {} exceeds {}".format(depth, max_depth), skill.path)
        )
    return issues


def _max_depth(root: str) -> int:
    best = 0
    root_parts = os.path.normpath(root).count(os.sep)
    for dirpath, dirnames, _filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        depth = os.path.normpath(dirpath).count(os.sep) - root_parts
        if depth > best:
            best = depth
    return best
