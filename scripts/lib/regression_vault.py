"""Append-only, parse-tolerant JSONL vault for findings.

Same pattern as .gmail's log.py — writes are monotonic; reads skip
unreadable lines rather than crashing.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Iterable, Iterator


REQUIRED_FIELDS = (
    "schema_version", "timestamp_iso", "round",
    "dimension", "severity", "message", "evidence",
)


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def append_finding(vault_path: str, finding: dict) -> None:
    """Append one finding dict to `vault_path/findings.jsonl` (schema-validated)."""
    finding = dict(finding)  # shallow copy
    finding.setdefault("schema_version", "0.1")
    finding.setdefault("timestamp_iso", _now_iso())
    finding.setdefault("round", 1)
    missing = [k for k in REQUIRED_FIELDS if k not in finding]
    if missing:
        raise ValueError("finding missing required fields: {}".format(missing))
    target = vault_path
    if os.path.isdir(vault_path) or not vault_path.endswith(".jsonl"):
        target = os.path.join(vault_path, "findings.jsonl")
    _ensure_dir(target)
    with open(target, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(finding, ensure_ascii=False) + "\n")


def iter_findings(vault_path: str) -> Iterator[dict]:
    """Yield one dict per valid line. Invalid lines are skipped silently."""
    target = vault_path
    if os.path.isdir(vault_path) or not vault_path.endswith(".jsonl"):
        target = os.path.join(vault_path, "findings.jsonl")
    if not os.path.isfile(target):
        return
    with open(target, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def append_benchmark(vault_path: str, record: dict) -> None:
    """Append one benchmark record to `vault_path/benchmark.jsonl`."""
    record = dict(record)
    record.setdefault("schema_version", "0.1")
    record.setdefault("timestamp_iso", _now_iso())
    target = vault_path
    if os.path.isdir(vault_path) or not vault_path.endswith(".jsonl"):
        target = os.path.join(vault_path, "benchmark.jsonl")
    _ensure_dir(target)
    with open(target, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def iter_benchmark(vault_path: str) -> Iterable[dict]:
    target = vault_path
    if os.path.isdir(vault_path) or not vault_path.endswith(".jsonl"):
        target = os.path.join(vault_path, "benchmark.jsonl")
    if not os.path.isfile(target):
        return
    with open(target, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue
