from __future__ import annotations

import io
import os
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.lib.plugin_loader import discover_plugins  # noqa: E402


PLUGIN_TEMPLATE = textwrap.dedent('''
    import os, sys
    _ROOT = {root!r}
    if _ROOT not in sys.path:
        sys.path.insert(0, _ROOT)
    from dimensions._plugin_base import DimensionPlugin

    class P(DimensionPlugin):
        name = {name!r}
        def probe(self, target):
            return []
''')


class TestPluginCollision(unittest.TestCase):
    def test_collision_skipped_with_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for entry in ("01_alpha", "02_beta"):
                d = os.path.join(tmp, entry)
                os.makedirs(d)
                with open(os.path.join(d, "plugin.py"), "w") as fh:
                    fh.write(PLUGIN_TEMPLATE.format(root=_ROOT, name="dup_name"))
            buf = io.StringIO()
            with redirect_stderr(buf):
                plugins = discover_plugins(dimensions_dir=tmp)
            self.assertEqual(len(plugins), 1)
            self.assertEqual(plugins[0].name, "dup_name")
            self.assertIn("collision", buf.getvalue())

    def test_distinct_names_both_load(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for entry, name in (("01_a", "alpha"), ("02_b", "beta")):
                d = os.path.join(tmp, entry)
                os.makedirs(d)
                with open(os.path.join(d, "plugin.py"), "w") as fh:
                    fh.write(PLUGIN_TEMPLATE.format(root=_ROOT, name=name))
            plugins = discover_plugins(dimensions_dir=tmp)
            self.assertEqual({p.name for p in plugins}, {"alpha", "beta"})


if __name__ == "__main__":
    unittest.main()
