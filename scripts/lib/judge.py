"""Haiku judge invocation shared by dims 09-14.

Responsibilities:
  - Load the per-dim judge prompt (markdown)
  - Attach ephemeral cache_control to the system block
  - Call the wrapped client with temperature 0.0, max 512 output
  - Parse a JSON verdict envelope: {verdict, evidence, confidence}
  - Validate; return UNKNOWN on malformed
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, Optional

from scripts.lib.anthropic_client import AnthropicClient, estimate_cost_usd
from scripts.lib.cost_guard import CostBudgetExceeded, CostGuard
from scripts.lib.prompt_cache import as_cached_system


VALID_VERDICTS = ("PASS", "FAIL", "UNKNOWN")
DEFAULT_JUDGE_MODEL = "claude-haiku-4-5"
MAX_JUDGE_OUTPUT = 512


def load_judge_prompt(dim_dir: str) -> str:
    path = os.path.join(dim_dir, "judge_prompt.md")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return "You are a strict binary grader. Reply JSON only."


def _parse_envelope(text: str) -> Dict[str, Any]:
    """Pull the first JSON object out of `text` and validate keys."""
    if not text:
        return _unknown("empty judge response")
    # Fast path: pure JSON
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not m:
            return _unknown("no JSON object in judge response")
        try:
            data = json.loads(m.group(0))
        except (ValueError, TypeError):
            return _unknown("unparseable JSON in judge response")
    if not isinstance(data, dict):
        return _unknown("judge response not an object")
    verdict = str(data.get("verdict", "")).strip().upper()
    if verdict not in VALID_VERDICTS:
        return _unknown("invalid verdict: {!r}".format(data.get("verdict")))
    evidence = str(data.get("evidence", "")).strip() or "(no evidence)"
    try:
        conf = int(data.get("confidence", 3))
    except (ValueError, TypeError):
        conf = 3
    conf = max(1, min(5, conf))
    return {"verdict": verdict, "evidence": evidence, "confidence": conf}


def _unknown(reason: str) -> Dict[str, Any]:
    return {"verdict": "UNKNOWN", "evidence": reason, "confidence": 1}


def judge(
    client: AnthropicClient,
    judge_prompt: str,
    user_content: str,
    model: str = DEFAULT_JUDGE_MODEL,
    cost_guard: Optional[CostGuard] = None,
    max_tokens: int = MAX_JUDGE_OUTPUT,
) -> Dict[str, Any]:
    """Single judge call. Returns {verdict, evidence, confidence, usage}.

    If `cost_guard` is passed, the call is skipped with UNKNOWN if the
    estimated pre-call cost cannot fit the remaining budget. We estimate
    generously (as if no cache hit) to stay conservative.
    """
    if cost_guard is not None:
        # Pre-estimate: treat full system + user as fresh input.
        # ~4 chars/token is Anthropic's documented English approximation.
        est_input = max(1, (len(judge_prompt) + len(user_content)) // 4)
        est = estimate_cost_usd(model, est_input, max_tokens, 0)
        if not cost_guard.can_spend(est):
            return _unknown("cost budget exceeded before judge call")
    system = as_cached_system(judge_prompt, pad_to_cache=True)
    messages = [{"role": "user", "content": user_content}]
    try:
        resp = client.messages_create(
            model=model,
            messages=messages,
            system=system,
            max_tokens=max_tokens,
            temperature=0.0,
        )
    except CostBudgetExceeded as e:
        return _unknown("cost budget exceeded: {}".format(e))
    except Exception as e:  # noqa: BLE001
        return _unknown("judge call raised: {}".format(e))
    if cost_guard is not None:
        cost_guard.record(float(resp.get("cost_usd", 0.0)))
    parsed = _parse_envelope(str(resp.get("text", "")))
    parsed["usage"] = {
        "input_tokens": resp.get("input_tokens", 0),
        "output_tokens": resp.get("output_tokens", 0),
        "cached_input_tokens": resp.get("cached_input_tokens", 0),
        "cost_usd": resp.get("cost_usd", 0.0),
        "mock": resp.get("mock", False),
    }
    return parsed
