"""Sonnet executor invocation.

Runs a user prompt through Claude impersonating the skill-under-test.
The skill's SKILL.md is loaded as the system prompt (so the executor
behaves like the skill would when triggered by the dispatcher). The
output is returned to judge dimensions.
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

from scripts.lib.anthropic_client import AnthropicClient, estimate_cost_usd
from scripts.lib.cost_guard import CostBudgetExceeded, CostGuard


DEFAULT_EXECUTOR_MODEL = "claude-sonnet-4-5"
MAX_EXECUTOR_OUTPUT = 1024


def load_skill_md(skill_path: str) -> str:
    path = os.path.join(skill_path, "SKILL.md")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def execute(
    client: AnthropicClient,
    skill_md: str,
    user_prompt: str,
    model: str = DEFAULT_EXECUTOR_MODEL,
    cost_guard: Optional[CostGuard] = None,
    max_tokens: int = MAX_EXECUTOR_OUTPUT,
) -> Dict[str, Any]:
    """Run `user_prompt` through the skill. Returns {text, usage, error?}."""
    if cost_guard is not None:
        est_input = max(1, (len(skill_md) + len(user_prompt)) // 3)
        est = estimate_cost_usd(model, est_input, max_tokens, 0)
        if not cost_guard.can_spend(est):
            return {"text": "", "error": "cost budget exceeded before executor call"}
    system = skill_md or "You are a helpful assistant."
    messages = [{"role": "user", "content": user_prompt}]
    try:
        resp = client.messages_create(
            model=model,
            messages=messages,
            system=system,
            max_tokens=max_tokens,
            temperature=0.0,
        )
    except CostBudgetExceeded as e:
        return {"text": "", "error": "cost budget exceeded: {}".format(e)}
    except Exception as e:  # noqa: BLE001
        return {"text": "", "error": "executor call raised: {}".format(e)}
    if cost_guard is not None:
        cost_guard.record(float(resp.get("cost_usd", 0.0)))
    return {
        "text": str(resp.get("text", "")),
        "usage": {
            "input_tokens": resp.get("input_tokens", 0),
            "output_tokens": resp.get("output_tokens", 0),
            "cached_input_tokens": resp.get("cached_input_tokens", 0),
            "cost_usd": resp.get("cost_usd", 0.0),
            "mock": resp.get("mock", False),
        },
    }
