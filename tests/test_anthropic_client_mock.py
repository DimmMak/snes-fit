"""Verify AnthropicClient mock mode is deterministic + no network calls."""
from __future__ import annotations

import json
import os
import sys
import unittest

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.lib.anthropic_client import AnthropicClient, estimate_cost_usd  # noqa: E402


class TestAnthropicClientMock(unittest.TestCase):
    def test_mock_mode_forced_via_ctor(self) -> None:
        c = AnthropicClient(mock_mode=True)
        self.assertTrue(c.mock)
        self.assertIsNone(c.client)

    def test_mock_mode_env_var(self) -> None:
        old = os.environ.get("AUTO_TEST_MOCK")
        os.environ["AUTO_TEST_MOCK"] = "1"
        try:
            c = AnthropicClient()
            self.assertTrue(c.mock)
        finally:
            if old is None:
                del os.environ["AUTO_TEST_MOCK"]
            else:
                os.environ["AUTO_TEST_MOCK"] = old

    def test_mock_pass_keyword(self) -> None:
        c = AnthropicClient(mock_mode=True)
        resp = c.messages_create(
            model="claude-haiku-4-5",
            messages=[{"role": "user", "content": "normal prompt"}],
            system="judge",
        )
        data = json.loads(resp["text"])
        self.assertEqual(data["verdict"], "PASS")

    def test_mock_fail_keyword(self) -> None:
        c = AnthropicClient(mock_mode=True)
        resp = c.messages_create(
            model="claude-haiku-4-5",
            messages=[{"role": "user", "content": "fail_keyword trigger"}],
            system="judge",
        )
        data = json.loads(resp["text"])
        self.assertEqual(data["verdict"], "FAIL")

    def test_mock_unknown_keyword(self) -> None:
        c = AnthropicClient(mock_mode=True)
        resp = c.messages_create(
            model="claude-haiku-4-5",
            messages=[{"role": "user", "content": "unknown_keyword here"}],
            system="judge",
        )
        data = json.loads(resp["text"])
        self.assertEqual(data["verdict"], "UNKNOWN")

    def test_usage_tracked(self) -> None:
        c = AnthropicClient(mock_mode=True)
        c.messages_create(
            model="claude-haiku-4-5",
            messages=[{"role": "user", "content": "hi"}],
        )
        summary = c.usage_summary()
        self.assertEqual(summary["calls"], 1)
        self.assertGreater(summary["input_tokens"], 0)
        self.assertGreater(summary["output_tokens"], 0)
        self.assertGreaterEqual(summary["total_cost_usd"], 0.0)

    def test_estimate_cost_haiku(self) -> None:
        cost = estimate_cost_usd("claude-haiku-4-5", 1_000_000, 0, 0)
        # 1M haiku input tokens ≈ $0.80
        self.assertAlmostEqual(cost, 0.80, places=2)

    def test_estimate_cost_cached_cheap(self) -> None:
        cached = estimate_cost_usd("claude-haiku-4-5", 1_000_000, 0, 1_000_000)
        uncached = estimate_cost_usd("claude-haiku-4-5", 1_000_000, 0, 0)
        self.assertLess(cached, uncached)


if __name__ == "__main__":
    unittest.main()
