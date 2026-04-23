"""Dynamic discovery of dimension plugins.

Walks `dimensions/*/plugin.py`, imports each one, and returns an instance
per subclass of `DimensionPlugin` it finds.
"""
from __future__ import annotations

import importlib.util
import inspect
import os
import sys
from typing import List, Optional

# Allow running both as a package (from .snes-fit root) and as a bare script.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_AUTO_TEST_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
if _AUTO_TEST_ROOT not in sys.path:
    sys.path.insert(0, _AUTO_TEST_ROOT)

from dimensions._plugin_base import DimensionPlugin  # noqa: E402


def discover_plugins(dimensions_dir: Optional[str] = None,
                     enabled_ids: Optional[List[str]] = None) -> List[DimensionPlugin]:
    """Return instantiated plugins from every `dimensions/NN_*/plugin.py`.

    If `enabled_ids` is provided, only plugins whose dir name is in the list
    are returned.
    """
    if dimensions_dir is None:
        dimensions_dir = os.path.join(_AUTO_TEST_ROOT, "dimensions")
    plugins: List[DimensionPlugin] = []
    seen_names: set = set()
    if not os.path.isdir(dimensions_dir):
        return plugins

    for entry in sorted(os.listdir(dimensions_dir)):
        sub = os.path.join(dimensions_dir, entry)
        if not os.path.isdir(sub):
            continue
        if entry.startswith("_") or entry.startswith("."):
            continue
        if enabled_ids is not None and entry not in enabled_ids:
            continue
        plugin_py = os.path.join(sub, "plugin.py")
        if not os.path.isfile(plugin_py):
            continue
        mod_name = "snes_fit_dim_{}".format(entry)
        spec = importlib.util.spec_from_file_location(mod_name, plugin_py)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            continue
        for _name, obj in inspect.getmembers(module, inspect.isclass):
            if obj is DimensionPlugin:
                continue
            if issubclass(obj, DimensionPlugin) and not inspect.isabstract(obj):
                try:
                    instance = obj()
                except Exception:
                    continue
                pname = getattr(instance, "name", "") or entry
                if pname in seen_names:
                    sys.stderr.write(
                        "snes-fit: plugin name collision: {!r} already loaded; "
                        "skipping duplicate from {}\n".format(pname, entry)
                    )
                    continue
                seen_names.add(pname)
                plugins.append(instance)
    return plugins
