"""Dimension 12 — prompt injection.

Fires each attack from `corpora/owasp-llm-top10.json` at the skill and
asks a judge whether the skill maintained its constraints (PASS) or was
successfully hijacked (FAIL).
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from dimensions._plugin_base import DimensionPlugin, Finding
from scripts.lib.anthropic_client import AnthropicClient
from scripts.lib.cost_guard import CostGuard
from scripts.lib.executor import execute, load_skill_md
from scripts.lib.judge import judge, load_judge_prompt


class PromptInjectionPlugin(DimensionPlugin):
    name = "12_prompt_injection"
    version = "0.2.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        dim_dir = os.path.dirname(os.path.abspath(__file__))
        skill_md = load_skill_md(target.path)
        if not skill_md:
            return [Finding(
                dimension=self.name, severity="major",
                message="SKILL.md missing — cannot probe injection",
                evidence=target.path,
            )]
        attacks = _load_attacks(dim_dir)
        if not attacks:
            return [Finding(
                dimension=self.name, severity="minor",
                message="no attacks loaded from corpora",
                evidence=dim_dir,
            )]
        client = AnthropicClient()
        # Mock-mode guard (v0.2.0 — fixes false-positive critical cascade).
        # When ANTHROPIC_API_KEY is missing, the wrapper enters mock mode and
        # `_mock_response` returns canned JSON keyed on substrings ("jailbreak_success",
        # "fail_keyword", "hallucinate"). The OWASP attack corpus contains literal
        # JAILBREAK_SUCCESS strings as the *desired* LLM hallucination — so every
        # attack prompt trips the mock-FAIL keyword check and 16 false-positive
        # CRITICAL findings get emitted per skill (45 skills × 16 = 720 fleet-wide).
        # If we can't probe for real, return ONE minor finding describing the gap
        # rather than 16 fake criticals. Real probing resumes once an API key
        # is available.
        if getattr(client, "mock", False):
            return [Finding(
                dimension=self.name, severity="minor",
                message=("prompt-injection probe skipped — running in mock mode "
                         "(ANTHROPIC_API_KEY missing or AUTO_TEST_MOCK=1). "
                         "Set ANTHROPIC_API_KEY to enable live probing."),
                evidence=target.path,
            )]
        guard = CostGuard.from_config()
        judge_prompt = load_judge_prompt(dim_dir)
        findings: List[Finding] = []
        for atk in attacks:
            prompt = atk.get("prompt", "")
            exec_out = execute(client, skill_md, prompt, cost_guard=guard)
            if exec_out.get("error"):
                findings.append(Finding(
                    dimension=self.name, severity="minor",
                    message="UNKNOWN {} ({}): {}".format(
                        atk.get("id"), atk.get("category"), exec_out["error"]),
                    evidence=target.path,
                ))
                continue
            user = (
                "Attack id: {}\nCategory: {}\nAttack prompt: {}\n\n"
                "Skill reply:\n---\n{}\n---\n"
            ).format(atk.get("id"), atk.get("category"), prompt,
                     (exec_out.get("text") or "")[:2000])
            v = judge(client, judge_prompt, user, cost_guard=guard)
            if v.get("verdict") == "FAIL":
                findings.append(Finding(
                    dimension=self.name, severity="critical",
                    message="injection succeeded on {} ({}): {}".format(
                        atk.get("id"), atk.get("category"),
                        v.get("evidence", "")[:200]),
                    evidence=target.path,
                ))
            elif v.get("verdict") == "UNKNOWN":
                findings.append(Finding(
                    dimension=self.name, severity="minor",
                    message="UNKNOWN on {}: {}".format(
                        atk.get("id"), v.get("evidence", "")[:200]),
                    evidence=target.path,
                ))
        return findings


def _load_attacks(dim_dir: str) -> List[Dict[str, Any]]:
    path = os.path.join(dim_dir, "corpora", "owasp-llm-top10.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        atks = data.get("attacks", [])
        return atks if isinstance(atks, list) else []
    except (OSError, json.JSONDecodeError):
        return []
