"""Anthropic SDK wrapper with mock mode + cost tracking.

Mock mode fires when:
  - ANTHROPIC_API_KEY is missing, OR
  - AUTO_TEST_MOCK=1 is set, OR
  - caller passes mock_mode=True, OR
  - `anthropic` SDK is not installed.

In mock mode, `messages_create` returns canned JSON responses keyed on
keywords in the prompt so judge/executor tests stay deterministic.
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional


# Approx public pricing per million tokens (2026 Q1).
PRICING_USD_PER_MILLION = {
    "claude-sonnet-4-5": {"input": 3.0, "output": 15.0, "cached_read": 0.30},
    "claude-haiku-4-5":  {"input": 0.80, "output": 4.0, "cached_read": 0.08},
    # fallbacks for any unknown model id: treat as haiku-priced
    "_default":          {"input": 0.80, "output": 4.0, "cached_read": 0.08},
}


def estimate_cost_usd(model: str, input_tokens: int, output_tokens: int,
                      cached_input_tokens: int = 0) -> float:
    key = model if model in PRICING_USD_PER_MILLION else "_default"
    p = PRICING_USD_PER_MILLION[key]
    uncached_in = max(0, input_tokens - cached_input_tokens)
    cost = (
        (uncached_in / 1_000_000.0) * p["input"]
        + (cached_input_tokens / 1_000_000.0) * p["cached_read"]
        + (output_tokens / 1_000_000.0) * p["output"]
    )
    return round(cost, 6)


class AnthropicClient:
    """Thin wrapper. Single responsibility: call the API or return a mock."""

    def __init__(self, mock_mode: bool = False, api_key: Optional[str] = None):
        self.mock = bool(mock_mode) or os.getenv("AUTO_TEST_MOCK") == "1"
        self._total_input = 0
        self._total_output = 0
        self._total_cached_input = 0
        self._total_cost_usd = 0.0
        self._calls: List[Dict[str, Any]] = []
        self.client = None
        if self.mock:
            return
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            self.mock = True
            sys.stderr.write("[auto-test] ANTHROPIC_API_KEY missing; mock mode\n")
            return
        try:
            import anthropic  # type: ignore
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            self.mock = True
            sys.stderr.write("[auto-test] anthropic SDK missing; mock mode\n")

    # ------------------------------------------------------------------
    def messages_create(self,
                        model: str,
                        messages: List[Dict[str, Any]],
                        system: Optional[Any] = None,
                        max_tokens: int = 1024,
                        temperature: float = 0.0,
                        cache_control: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Return a dict of shape {text, input_tokens, output_tokens,
        cached_input_tokens, cost_usd, mock}.

        `system` may be a string (plain) or a list of content blocks (already
        shaped with cache_control). If `cache_control` is passed alongside a
        string `system`, we wrap it into a list form.
        """
        sys_payload = self._build_system(system, cache_control)
        if self.mock:
            return self._record(self._mock_response(model, messages, sys_payload))
        # Real SDK call
        kwargs: Dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }
        if sys_payload is not None:
            kwargs["system"] = sys_payload
        resp = self.client.messages.create(**kwargs)  # type: ignore[union-attr]
        text = ""
        try:
            for block in resp.content:
                if getattr(block, "type", None) == "text":
                    text += block.text
        except Exception:
            text = str(resp)
        usage = getattr(resp, "usage", None)
        input_tokens = getattr(usage, "input_tokens", 0) or 0
        output_tokens = getattr(usage, "output_tokens", 0) or 0
        cached_input_tokens = (
            getattr(usage, "cache_read_input_tokens", 0) or 0
        )
        return self._record({
            "text": text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cached_input_tokens": cached_input_tokens,
            "model": model,
            "mock": False,
        })

    # ------------------------------------------------------------------
    def _build_system(self, system: Any, cache_control: Optional[Dict[str, Any]]) -> Any:
        if system is None:
            return None
        if isinstance(system, list):
            return system
        if cache_control:
            return [{"type": "text", "text": str(system), "cache_control": cache_control}]
        return system

    def _record(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        input_tokens = int(raw.get("input_tokens", 0))
        output_tokens = int(raw.get("output_tokens", 0))
        cached = int(raw.get("cached_input_tokens", 0))
        model = str(raw.get("model", "_default"))
        cost = estimate_cost_usd(model, input_tokens, output_tokens, cached)
        self._total_input += input_tokens
        self._total_output += output_tokens
        self._total_cached_input += cached
        self._total_cost_usd += cost
        raw["cost_usd"] = cost
        self._calls.append({
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cached_input_tokens": cached,
            "cost_usd": cost,
        })
        return raw

    # ------------------------------------------------------------------
    def _mock_response(self, model: str, messages: List[Dict[str, Any]],
                        system: Any) -> Dict[str, Any]:
        blob = json.dumps(messages) + "|" + json.dumps(system or "")
        low = blob.lower()
        if "fail_keyword" in low or "hallucinate" in low or "jailbreak_success" in low:
            verdict = "FAIL"
        elif "unknown_keyword" in low:
            verdict = "UNKNOWN"
        else:
            verdict = "PASS"
        text = json.dumps({
            "verdict": verdict,
            "evidence": "[mock] deterministic response for testing",
            "confidence": 5,
        })
        return {
            "text": text,
            "input_tokens": 100,
            "output_tokens": 50,
            "cached_input_tokens": 0,
            "model": model,
            "mock": True,
        }

    # ------------------------------------------------------------------
    @property
    def total_cost_usd(self) -> float:
        return round(self._total_cost_usd, 6)

    @property
    def call_log(self) -> List[Dict[str, Any]]:
        return list(self._calls)

    def usage_summary(self) -> Dict[str, Any]:
        return {
            "calls": len(self._calls),
            "input_tokens": self._total_input,
            "output_tokens": self._total_output,
            "cached_input_tokens": self._total_cached_input,
            "total_cost_usd": self.total_cost_usd,
            "mock": self.mock,
        }
