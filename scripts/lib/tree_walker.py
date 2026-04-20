"""Fleet discovery + structural introspection.

Walks a fleet root (default `~/Desktop/CLAUDE CODE/`) and returns one
`SkillInfo` per directory that looks like a skill (contains SKILL.md).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional


CANONICAL_SUBDIRS = ("scripts", "config", "prompts", "tests", "dimensions", "logs")

# Directories that should NEVER be scanned as skill content.
# Vendored deps, build artifacts, VCS metadata, caches. Every file-walking
# dimension plugin should call prune_excluded_dirs(dirnames) in its os.walk
# loop to skip these.
EXCLUDED_DIRS = frozenset({
    # Python
    "__pycache__", ".venv", "venv", "env", ".tox", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "egg-info",
    # JS / TS
    "node_modules", ".next", ".nuxt", ".turbo", ".parcel-cache",
    "bower_components",
    # Build artifacts
    "dist", "build", "target", "out", ".cache", ".gradle",
    # VCS
    ".git", ".hg", ".svn",
    # IDE
    ".idea", ".vscode", ".vs",
    # OS
    ".DS_Store",
    # Archive dumps
    "_archive", "_archive-2026-04-19",
})

# File suffixes that indicate generated/binary/minified content.
EXCLUDED_FILE_SUFFIXES = (
    ".min.js", ".min.css", ".map",
    ".pyc", ".pyo",
    ".so", ".dylib", ".dll",
    ".class",
    ".lock", "-lock.json", "-lock.yaml",  # package-lock.json, yarn.lock, uv.lock, etc.
)


def prune_excluded_dirs(dirnames: List[str]) -> None:
    """Mutate dirnames IN PLACE to remove excluded + hidden dirs.

    Call this inside every os.walk loop so walks don't descend into
    node_modules, __pycache__, .git, etc.
    """
    dirnames[:] = [
        d for d in dirnames
        if d not in EXCLUDED_DIRS and not d.startswith(".")
    ]


def is_excluded_file(filename: str) -> bool:
    """True if filename is a build/binary/lock artifact we should skip."""
    lname = filename.lower()
    return any(lname.endswith(suf) for suf in EXCLUDED_FILE_SUFFIXES)


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


def _load_excluded_skill_names() -> set:
    """Read config/excluded-skills.json — repos that look like skills but aren't.

    Returns a set of directory names to skip during fleet discovery.
    Silently returns empty set if the config is missing or malformed
    (graceful degradation — never crash discover_skills on a config bug).
    """
    import json
    cfg_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        os.pardir, os.pardir, "config", "excluded-skills.json",
    )
    cfg_path = os.path.abspath(cfg_path)
    if not os.path.isfile(cfg_path):
        return set()
    try:
        with open(cfg_path, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return set()
    out: set = set()
    for entry in doc.get("excluded", []):
        if isinstance(entry, dict) and entry.get("name"):
            out.add(entry["name"])
        elif isinstance(entry, str):
            out.add(entry)
    return out


def discover_skills(root: str) -> List[SkillInfo]:
    """Return one SkillInfo per direct child of `root` that contains SKILL.md.

    Honors config/excluded-skills.json — any repo listed there is skipped
    (for repos that live under ~/Desktop/CLAUDE CODE/ but aren't skills:
    blue-hill-capital, claude-sessions, DimmMak.github.io, etc.).
    """
    results: List[SkillInfo] = []
    if not os.path.isdir(root):
        return results
    excluded_names = _load_excluded_skill_names()
    for entry in sorted(os.listdir(root)):
        full = os.path.join(root, entry)
        if not os.path.isdir(full):
            continue
        if entry.startswith(".") or entry.startswith("_"):
            continue
        if entry in excluded_names:
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
        prune_excluded_dirs(dirnames)
        for fn in filenames:
            if is_excluded_file(fn):
                continue
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
        prune_excluded_dirs(dirnames)
        depth = os.path.normpath(dirpath).count(os.sep) - root_parts
        if depth > best:
            best = depth
    return best
