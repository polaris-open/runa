"""Tests for runa.vault."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from runa import vault  # noqa: E402


class ListMarkdownFilesTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        # Real content.
        (self.root / "notes").mkdir()
        (self.root / "projects").mkdir()
        (self.root / "notes" / "a.md").write_text("# A\n", encoding="utf-8")
        (self.root / "projects" / "b.md").write_text("# B\n", encoding="utf-8")
        (self.root / "inbox.md").write_text("# Inbox\n", encoding="utf-8")
        (self.root / "notes" / "not-markdown.txt").write_text("x\n", encoding="utf-8")
        # Ignored directories, each with a Markdown file inside.
        for ignored in (".git", ".obsidian", "proposals", "__pycache__"):
            (self.root / ignored).mkdir()
            (self.root / ignored / "ignored.md").write_text("# nope\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_counts_only_markdown(self):
        files = vault.list_markdown_files(self.root)
        names = {p.name for p in files}
        self.assertEqual(names, {"a.md", "b.md", "inbox.md"})
        self.assertEqual(len(files), 3)

    def test_ignores_git(self):
        files = vault.list_markdown_files(self.root)
        self.assertFalse(any(".git" in p.parts for p in files))

    def test_ignores_obsidian(self):
        files = vault.list_markdown_files(self.root)
        self.assertFalse(any(".obsidian" in p.parts for p in files))

    def test_ignores_proposals(self):
        files = vault.list_markdown_files(self.root)
        self.assertFalse(any("proposals" in p.parts for p in files))

    def test_scan_vault_summary(self):
        summary = vault.scan_vault(self.root)
        self.assertEqual(summary["markdown_files"], 3)
        self.assertIn("notes", summary["top_level_directories"])
        self.assertIn("projects", summary["top_level_directories"])
        self.assertNotIn("proposals", summary["top_level_directories"])
        self.assertNotIn(".git", summary["top_level_directories"])

    def test_resolve_missing_vault_raises(self):
        with self.assertRaises(FileNotFoundError):
            vault.resolve_vault(self.root / "does-not-exist")


if __name__ == "__main__":
    unittest.main()
