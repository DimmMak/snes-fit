"""Dimension 09 — LLM output quality.

Runs a sample user prompt through the skill-under-test (Sonnet executor),
then asks a Haiku judge whether the output honors SKILL.md's stated
capabilities. Binary PASS/FAIL/UNKNOWN.

No API key -> UNKNOWN verdict (dim skips gracefully).
Mock mode -> deterministic PASS via anthropic_client mock.
"""
from __future__ import annotations

import os
from typing import List

from dimensions._plugin_base import DimensionPlugin, Finding
from scripts.lib.anthropic_client import AnthropicClient
from scripts.lib.cost_guard import CostGuard
from scripts.lib.executor import execute, load_skill_md
from scripts.lib.judge import judge, load_judge_prompt


SAMPLE_PROMPT = (
    "Given your stated purpose in the system prompt, produce one concrete "
    "example of the kind of output you were designed to produce. Keep it short."
)


class LLMOutputQualityPlugin(DimensionPlugin):
    name = "09_llm_output_quality"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        dim_dir = os.path.dirname(os.path.abspath(__file__))
        skill_md = load_skill_md(target.path)
        if not skill_md:
            return [Finding(
                dimension=self.name, severity="major",
                message="SKILL.md missing — cannot run output-quality eval",
                evidence=target.path,
            )]
        client = AnthropicClient()
        guard = CostGuard.from_config()
        # Step 1: executor produces output
        exec_out = execute(client, skill_md, SAMPLE_PROMPT, cost_guard=guard)
        if exec_out.get("error"):
            return [_unknown_finding(self.name, exec_out["error"], target.path)]
        # Step 2: judge scores output
        judge_prompt = load_judge_prompt(dim_dir)
        user = (
            "SKILL.md (stated purpose):\n---\n"
            + skill_md[:4000]
            + "\n---\n\nSKILL OUTPUT to grade:\n---\n"
            + (exec_out.get("text", "") or "(empty)")[:4000]
            + "\n---\n"
        )
        verdict = judge(client, judge_prompt, user, cost_guard=guard)
        return _verdict_to_findings(self.name, verdict, target.path)


def _verdict_to_findings(dim: str, verdict: dict, evidence_path: str) -> List[Finding]:
    v = verdict.get("verdict", "UNKNOWN")
    msg = verdict.get("evidence", "(no evidence)")
    if v == "PASS":
        return []
    sev = "major" if v == "FAIL" else "minor"
    return [Finding(
        dimension=dim, severity=sev,
        message="judge verdict {}: {}".format(v, msg[:200]),
        evidence=evidence_path,
    )]


def _unknown_finding(dim: str, reason: str, path: str) -> Finding:
    return Finding(
        dimension=dim, severity="minor",
        message="UNKNOWN: {}".format(reason),
        evidence=path,
    )
