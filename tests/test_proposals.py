"""Tests for runa.proposals."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from runa import proposals  # noqa: E402


class ProposalsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        # An existing note we expect to remain untouched.
        (self.root / "notes").mkdir()
        self.note = self.root / "notes" / "existing.md"
        self.note.write_text("# Existing\n\nOriginal content.\n", encoding="utf-8")
        self._note_before = self.note.read_text(encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_creates_file_inside_proposals(self):
        path = proposals.create_proposal(self.root, "Improve project status note", "Body.")
        self.assertTrue(path.exists())
        self.assertEqual(path.parent.name, "proposals")
        self.assertTrue(path.name.endswith(".md"))

    def test_title_and_status_in_content(self):
        path = proposals.create_proposal(self.root, "Improve project status note", "Body.")
        text = path.read_text(encoding="utf-8")
        self.assertIn("Improve project status note", text)
        self.assertIn("proposed", text)
        self.assertIn("Body.", text)

    def test_does_not_modify_existing_notes(self):
        proposals.create_proposal(self.root, "Some change", "Body.")
        self.assertEqual(self.note.read_text(encoding="utf-8"), self._note_before)

    def test_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            proposals.create_proposal(self.root, "   ", "Body.")

    def test_slugify(self):
        self.assertEqual(proposals.slugify("Hello, World!"), "hello-world")
        self.assertEqual(proposals.slugify("   "), "proposal")


if __name__ == "__main__":
    unittest.main()
