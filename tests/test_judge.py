"""Judge invocation: parsing, validation, UNKNOWN fallbacks."""
from __future__ import annotations

import os
import sys
import unittest

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.lib.anthropic_client import AnthropicClient  # noqa: E402
from scripts.lib.cost_guard import CostGuard  # noqa: E402
from scripts.lib.judge import _parse_envelope, judge  # noqa: E402


class TestJudgeParseEnvelope(unittest.TestCase):
    def test_valid_pass(self) -> None:
        out = _parse_envelope('{"verdict":"PASS","evidence":"ok","confidence":4}')
        self.assertEqual(out["verdict"], "PASS")
        self.assertEqual(out["confidence"], 4)

    def test_valid_fail(self) -> None:
        out = _parse_envelope('{"verdict":"FAIL","evidence":"broken"}')
        self.assertEqual(out["verdict"], "FAIL")
        self.assertEqual(out["confidence"], 3)

    def test_empty_returns_unknown(self) -> None:
        out = _parse_envelope("")
        self.assertEqual(out["verdict"], "UNKNOWN")

    def test_invalid_verdict(self) -> None:
        out = _parse_envelope('{"verdict":"MAYBE","evidence":"x"}')
        self.assertEqual(out["verdict"], "UNKNOWN")

    def test_malformed_json(self) -> None:
        out = _parse_envelope("not json at all")
        self.assertEqual(out["verdict"], "UNKNOWN")

    def test_embedded_json(self) -> None:
        out = _parse_envelope('Sure! {"verdict":"PASS","evidence":"ok"} done.')
        self.assertEqual(out["verdict"], "PASS")

    def test_confidence_clamped_low(self) -> None:
        out = _parse_envelope('{"verdict":"PASS","evidence":"x","confidence":-3}')
        self.assertEqual(out["confidence"], 1)

    def test_confidence_clamped_high(self) -> None:
        out = _parse_envelope('{"verdict":"PASS","evidence":"x","confidence":99}')
        self.assertEqual(out["confidence"], 5)


class TestJudgeCall(unittest.TestCase):
    def test_mock_returns_pass(self) -> None:
        client = AnthropicClient(mock_mode=True)
        out = judge(client, "judge prompt here", "benign user content")
        self.assertEqual(out["verdict"], "PASS")
        self.assertIn("usage", out)

    def test_mock_returns_fail_on_keyword(self) -> None:
        client = AnthropicClient(mock_mode=True)
        out = judge(client, "judge prompt", "this contains fail_keyword")
        self.assertEqual(out["verdict"], "FAIL")

    def test_cost_guard_blocks_when_over_budget(self) -> None:
        client = AnthropicClient(mock_mode=True)
        guard = CostGuard(max_usd=0.0)  # zero budget
        out = judge(client, "p", "u", cost_guard=guard)
        self.assertEqual(out["verdict"], "UNKNOWN")
        self.assertIn("budget", out["evidence"].lower())


if __name__ == "__main__":
    unittest.main()
