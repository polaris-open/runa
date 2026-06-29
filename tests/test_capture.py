"""Tests for runa.capture (append-only inbox)."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from runa import capture  # noqa: E402


class CaptureTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_creates_inbox_when_absent(self):
        inbox = capture.capture(self.root, "First synthetic note.")
        self.assertTrue(inbox.exists())
        text = inbox.read_text(encoding="utf-8")
        self.assertIn("# Inbox", text)
        self.assertIn("First synthetic note.", text)

    def test_appends_without_rewriting(self):
        capture.capture(self.root, "Entry one.")
        inbox = capture.capture(self.root, "Entry two.")
        text = inbox.read_text(encoding="utf-8")
        self.assertIn("Entry one.", text)
        self.assertIn("Entry two.", text)
        # Heading is written exactly once.
        self.assertEqual(text.count("# Inbox"), 1)

    def test_rejects_empty_text(self):
        with self.assertRaises(ValueError):
            capture.capture(self.root, "   ")

    def test_does_not_write_outside_vault(self):
        with self.assertRaises(ValueError):
            capture.capture(self.root, "escape", inbox_name="../escape.md")


if __name__ == "__main__":
    unittest.main()
