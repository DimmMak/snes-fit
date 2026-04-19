from __future__ import annotations

import os
import sys
import tempfile
import unittest

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.lib import tree_walker  # noqa: E402


class TestTreeWalker(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        # Make two fake skills
        for name in ("alpha", "beta"):
            os.makedirs(os.path.join(self.root, name, "scripts"))
            with open(os.path.join(self.root, name, "SKILL.md"), "w") as fh:
                fh.write("# {}\n".format(name))
            with open(os.path.join(self.root, name, "scripts", "a.py"), "w") as fh:
                fh.write("x = 1\n")
        # A non-skill dir
        os.makedirs(os.path.join(self.root, "notaskill"))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_discover_finds_skills(self) -> None:
        skills = tree_walker.discover_skills(self.root)
        names = {s.name for s in skills}
        self.assertIn("alpha", names)
        self.assertIn("beta", names)
        self.assertIn("notaskill", names)

    def test_has_skill_md_flag(self) -> None:
        skills = {s.name: s for s in tree_walker.discover_skills(self.root)}
        self.assertTrue(skills["alpha"].has_skill_md)
        self.assertFalse(skills["notaskill"].has_skill_md)

    def test_get_skill_none(self) -> None:
        self.assertIsNone(tree_walker.get_skill(self.root, "doesnotexist"))

    def test_validate_tree_missing_skill_md(self) -> None:
        s = tree_walker.get_skill(self.root, "notaskill")
        self.assertIsNotNone(s)
        issues = tree_walker.validate_tree(s)
        kinds = {i.kind for i in issues}
        self.assertIn("missing_skill_md", kinds)


if __name__ == "__main__":
    unittest.main()
