"""Dimension 13 — contract drift.

Reads SKILL.md's `composable_with:` YAML list. For each paired skill,
asks the judge whether skill A's declared output shape matches skill B's
declared input shape. Catches silent drift after independent updates.
"""
from __future__ import annotations

import os
import re
from typing import List, Optional

from dimensions._plugin_base import DimensionPlugin, Finding
from scripts.lib.anthropic_client import AnthropicClient
from scripts.lib.cost_guard import CostGuard
from scripts.lib.executor import load_skill_md
from scripts.lib.judge import judge, load_judge_prompt


_COMPOSABLE_RX = re.compile(
    r"composable_with\s*:\s*\n((?:\s*-\s*.+\n?)+)",
    re.IGNORECASE,
)
_LIST_ITEM_RX = re.compile(r"-\s*[\"']?([^\"'\n]+?)[\"']?\s*$", re.MULTILINE)


class ContractDriftPlugin(DimensionPlugin):
    name = "13_contract_drift"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        dim_dir = os.path.dirname(os.path.abspath(__file__))
        skill_md_a = load_skill_md(target.path)
        if not skill_md_a:
            return [Finding(
                dimension=self.name, severity="major",
                message="SKILL.md missing — cannot probe contracts",
                evidence=target.path,
            )]
        peers = _extract_composable_with(skill_md_a)
        if not peers:
            return []  # nothing to check is not a failure
        fleet_root = os.path.dirname(target.path)
        client = AnthropicClient()
        guard = CostGuard.from_config()
        judge_prompt = load_judge_prompt(dim_dir)
        findings: List[Finding] = []
        for peer in peers:
            peer_md = _load_peer_skill_md(fleet_root, peer)
            if peer_md is None:
                findings.append(Finding(
                    dimension=self.name, severity="minor",
                    message="declared peer {!r} not found on disk".format(peer),
                    evidence=fleet_root,
                ))
                continue
            user = (
                "Skill A ({}) SKILL.md:\n---\n{}\n---\n\n"
                "Skill B ({}) SKILL.md:\n---\n{}\n---\n"
            ).format(target.name, skill_md_a[:4000], peer, peer_md[:4000])
            v = judge(client, judge_prompt, user, cost_guard=guard)
            if v.get("verdict") == "FAIL":
                findings.append(Finding(
                    dimension=self.name, severity="major",
                    message="contract drift with {!r}: {}".format(
                        peer, v.get("evidence", "")[:200]),
                    evidence=target.path,
                ))
            elif v.get("verdict") == "UNKNOWN":
                findings.append(Finding(
                    dimension=self.name, severity="minor",
                    message="UNKNOWN vs {!r}: {}".format(
                        peer, v.get("evidence", "")[:200]),
                    evidence=target.path,
                ))
        return findings


def _extract_composable_with(skill_md: str) -> List[str]:
    m = _COMPOSABLE_RX.search(skill_md or "")
    if not m:
        return []
    block = m.group(1)
    items = [x.strip() for x in _LIST_ITEM_RX.findall(block)]
    return [i for i in items if i]


def _load_peer_skill_md(fleet_root: str, peer_name: str) -> Optional[str]:
    path = os.path.join(fleet_root, peer_name, "SKILL.md")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None
