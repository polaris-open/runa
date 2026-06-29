"""Tests for runa.config."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from runa import config  # noqa: E402


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_detects_existing_config(self):
        (self.root / "runa.yaml").write_text('version: "0.1"\n', encoding="utf-8")
        found = config.find_config(self.root)
        self.assertIsNotNone(found)
        loaded = config.load_config(self.root)
        self.assertTrue(loaded["exists"])
        self.assertIsNotNone(loaded["raw"])

    def test_missing_config_does_not_break(self):
        self.assertIsNone(config.find_config(self.root))
        loaded = config.load_config(self.root)
        self.assertFalse(loaded["exists"])
        self.assertIsNone(loaded["path"])
        self.assertIsNone(loaded["raw"])


if __name__ == "__main__":
    unittest.main()
