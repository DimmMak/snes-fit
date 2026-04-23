"""Dimension 10 — trigger precision.

Checks whether SKILL.md's description correctly triggers on true-positive
prompts and correctly REFUSES on collision/false-positive prompts.

Test corpus:
  - evals/<skill>/trigger-tests.json   (preferred; authored by user)
  - else auto-generated from SKILL.md's "NOT for" clauses + one vanilla
    positive prompt.

Each prompt is run through the executor (Sonnet with SKILL.md as system);
Haiku judges whether the skill's behaviour matches `should_trigger`.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional

from dimensions._plugin_base import DimensionPlugin, Finding
from scripts.lib.anthropic_client import AnthropicClient
from scripts.lib.cost_guard import CostGuard
from scripts.lib.executor import execute, load_skill_md
from scripts.lib.judge import judge, load_judge_prompt


class TriggerPrecisionPlugin(DimensionPlugin):
    name = "10_trigger_precision"
    version = "0.1.0"
    runs_on = "skill"

    def probe(self, target) -> List[Finding]:
        dim_dir = os.path.dirname(os.path.abspath(__file__))
        skill_md = load_skill_md(target.path)
        if not skill_md:
            return [Finding(
                dimension=self.name, severity="major",
                message="SKILL.md missing — cannot probe triggers",
                evidence=target.path,
            )]
        tests = _load_or_generate_tests(target, skill_md)
        if not tests:
            return [Finding(
                dimension=self.name, severity="minor",
                message="no trigger tests found or generated",
                evidence=target.path,
            )]
        client = AnthropicClient()
        guard = CostGuard.from_config()
        judge_prompt = load_judge_prompt(dim_dir)
        findings: List[Finding] = []
        for test in tests:
            prompt = test.get("prompt", "")
            expected = bool(test.get("should_trigger", True))
            exec_out = execute(client, skill_md, prompt, cost_guard=guard)
            if exec_out.get("error"):
                findings.append(Finding(
                    dimension=self.name, severity="minor",
                    message="UNKNOWN for prompt {!r}: {}".format(prompt[:60], exec_out["error"]),
                    evidence=target.path,
                ))
                continue
            user = (
                "Prompt: {}\n\n"
                "Expected should_trigger: {}\n\n"
                "Skill's reply:\n---\n{}\n---\n"
            ).format(prompt, expected, (exec_out.get("text") or "")[:2000])
            v = judge(client, judge_prompt, user, cost_guard=guard)
            if v.get("verdict") == "FAIL":
                findings.append(Finding(
                    dimension=self.name, severity="major",
                    message="trigger mismatch on {!r}: {}".format(
                        prompt[:60], v.get("evidence", "")[:200]),
                    evidence=target.path,
                ))
            elif v.get("verdict") == "UNKNOWN":
                findings.append(Finding(
                    dimension=self.name, severity="minor",
                    message="UNKNOWN on {!r}: {}".format(
                        prompt[:60], v.get("evidence", "")[:200]),
                    evidence=target.path,
                ))
        return findings


def _load_or_generate_tests(target, skill_md: str) -> List[Dict[str, Any]]:
    # Preferred: evals/<skill>/trigger-tests.json anchored at the snes-fit root.
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", ".."))
    user_file = os.path.join(root, "evals", target.name, "trigger-tests.json")
    if os.path.isfile(user_file):
        try:
            with open(user_file, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            tests = data.get("tests") if isinstance(data, dict) else data
            if isinstance(tests, list):
                return tests
        except (OSError, json.JSONDecodeError):
            pass
    # Fallback: auto-generate.
    return _auto_generate_tests(skill_md)


_NOT_FOR_RX = re.compile(r"NOT\s+for:\s*([^.\n]+)", re.IGNORECASE)


def _auto_generate_tests(skill_md: str) -> List[Dict[str, Any]]:
    positives: List[Dict[str, Any]] = [{
        "prompt": "Please do what this skill does — one short example.",
        "should_trigger": True,
    }]
    negatives: List[Dict[str, Any]] = []
    for m in _NOT_FOR_RX.finditer(skill_md or ""):
        phrase = m.group(1).strip().rstrip(")").strip()
        if not phrase:
            continue
        negatives.append({
            "prompt": "Help me with: {}".format(phrase),
            "should_trigger": False,
        })
        if len(negatives) >= 3:
            break
    return positives + negatives
