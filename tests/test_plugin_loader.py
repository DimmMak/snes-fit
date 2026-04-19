from __future__ import annotations

import os
import sys
import unittest

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.lib.plugin_loader import discover_plugins  # noqa: E402
from dimensions._plugin_base import DimensionPlugin  # noqa: E402


class TestPluginLoader(unittest.TestCase):
    def test_discovers_all_fourteen(self) -> None:
        plugins = discover_plugins()
        names = {p.name for p in plugins}
        expected = {
            # phase 1
            "01_adversarial", "02_scale", "03_composition", "04_security",
            "05_threat_intel", "06_types", "07_structural", "08_design_audit",
            # phase 2 (LLM-eval)
            "09_llm_output_quality", "10_trigger_precision",
            "11_hallucination_probe", "12_prompt_injection",
            "13_contract_drift", "14_llm_self_audit",
        }
        self.assertEqual(names, expected)

    def test_all_subclass_base(self) -> None:
        plugins = discover_plugins()
        for p in plugins:
            self.assertIsInstance(p, DimensionPlugin)

    def test_enabled_filter(self) -> None:
        plugins = discover_plugins(enabled_ids=["08_design_audit"])
        self.assertEqual(len(plugins), 1)
        self.assertEqual(plugins[0].name, "08_design_audit")


if __name__ == "__main__":
    unittest.main()
