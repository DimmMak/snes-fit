"""Dimension 14 — LLM self-audit.

Meta-dimension: feeds SKILL.md + ARCHITECTURE.md (and NON_GOALS.md if
present) to a judge and asks "does this skill honor its declared
invariants and non-goals?"
"""
from __future__ import annotations

import os
from typing import List, Optional

from dimensions._plugin_base import DimensionPlugin, Finding
from scripts.lib.anthropic_client import AnthropicClient
from scripts.lib.cost_guard import CostGuard
from scripts.lib.judge import judge, load_judge_prompt


class LLMSelfAuditPlugin(DimensionPlugin):
    name = "14_llm_self_audit"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        dim_dir = os.path.dirname(os.path.abspath(__file__))
        skill_md = _read(os.path.join(target.path, "SKILL.md"))
        if not skill_md:
            return [Finding(
                dimension=self.name, severity="major",
                message="SKILL.md missing — cannot self-audit",
                evidence=target.path,
            )]
        arch = _read(os.path.join(target.path, "ARCHITECTURE.md")) or "(none)"
        nong = _read(os.path.join(target.path, "NON_GOALS.md")) or "(none)"
        client = AnthropicClient()
        guard = CostGuard.from_config()
        judge_prompt = load_judge_prompt(dim_dir)
        user = (
            "SKILL.md:\n---\n{}\n---\n\n"
            "ARCHITECTURE.md:\n---\n{}\n---\n\n"
            "NON_GOALS.md:\n---\n{}\n---\n"
        ).format(skill_md[:6000], arch[:4000], nong[:2000])
        v = judge(client, judge_prompt, user, cost_guard=guard)
        verdict = v.get("verdict", "UNKNOWN")
        if verdict == "PASS":
            return []
        if verdict == "FAIL":
            return [Finding(
                dimension=self.name, severity="major",
                message="self-audit FAIL: {}".format(v.get("evidence", "")[:240]),
                evidence=target.path,
            )]
        return [Finding(
            dimension=self.name, severity="minor",
            message="self-audit UNKNOWN: {}".format(v.get("evidence", "")[:240]),
            evidence=target.path,
        )]


def _read(path: str) -> Optional[str]:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None
