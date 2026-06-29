"""Path-security tests: traversal, absolute escape, symlink escape, unicode."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from runa import capture, proposals, safety  # noqa: E402


class EnsurePathInsideVaultTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name) / "vault"
        self.vault.mkdir()
        self._outside = tempfile.TemporaryDirectory()
        self.outside = Path(self._outside.name)

    def tearDown(self):
        self._tmp.cleanup()
        self._outside.cleanup()

    def test_normal_path_allowed(self):
        target = safety.ensure_path_inside_vault(self.vault / "notes" / "a.md", self.vault)
        self.assertTrue(str(target).startswith(str(self.vault.resolve())))

    def test_vault_root_allowed(self):
        self.assertEqual(
            safety.ensure_path_inside_vault(self.vault, self.vault),
            self.vault.resolve(),
        )

    def test_dotdot_traversal_rejected(self):
        with self.assertRaises(ValueError):
            safety.ensure_path_inside_vault(self.vault / ".." / "secret.md", self.vault)

    def test_absolute_outside_rejected(self):
        with self.assertRaises(ValueError):
            safety.ensure_path_inside_vault("/etc/passwd", self.vault)

    def test_symlink_file_escape_rejected(self):
        secret = self.outside / "secret.md"
        secret.write_text("synthetic secret\n", encoding="utf-8")
        link = self.vault / "link.md"
        os.symlink(secret, link)
        with self.assertRaises(ValueError):
            safety.ensure_path_inside_vault(link, self.vault)

    def test_symlink_dir_escape_rejected(self):
        link_dir = self.vault / "linkdir"
        os.symlink(self.outside, link_dir)
        with self.assertRaises(ValueError):
            safety.ensure_path_inside_vault(link_dir / "x.md", self.vault)


class CaptureMaliciousInboxTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name) / "vault"
        self.vault.mkdir()
        self._outside = tempfile.TemporaryDirectory()
        self.outside = Path(self._outside.name)

    def tearDown(self):
        self._tmp.cleanup()
        self._outside.cleanup()

    def test_traversal_inbox_rejected_and_no_file_written(self):
        escape = self.outside / "escape.md"
        with self.assertRaises(ValueError):
            capture.capture(self.vault, "hello", inbox_name="../escape.md")
        self.assertFalse(escape.exists())

    def test_absolute_inbox_rejected(self):
        escape = self.outside / "abs.md"
        with self.assertRaises(ValueError):
            capture.capture(self.vault, "hello", inbox_name=str(escape))
        self.assertFalse(escape.exists())

    def test_unicode_and_spaces_text(self):
        inbox = capture.capture(self.vault, "Reunião com a equipe — café ☕ às 9h")
        self.assertTrue(inbox.exists())
        self.assertIn("café ☕", inbox.read_text(encoding="utf-8"))


class ProposalsMaliciousDirTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name) / "vault"
        self.vault.mkdir()
        self._outside = tempfile.TemporaryDirectory()
        self.outside = Path(self._outside.name)

    def tearDown(self):
        self._tmp.cleanup()
        self._outside.cleanup()

    def test_traversal_proposals_dir_rejected_no_dir_created(self):
        # "../evil" would resolve to a sibling of the vault; it must not be created.
        escape = self.vault.parent / "evil"
        with self.assertRaises(ValueError):
            proposals.create_proposal(self.vault, "t", proposals_dir="../evil")
        self.assertFalse(escape.exists())

    def test_absolute_proposals_dir_rejected(self):
        target = self.outside / "evil"
        with self.assertRaises(ValueError):
            proposals.create_proposal(self.vault, "t", proposals_dir=str(target))
        self.assertFalse(target.exists())

    def test_symlinked_proposals_dir_rejected(self):
        # proposals/ is a symlink pointing outside the vault.
        os.symlink(self.outside, self.vault / "proposals")
        with self.assertRaises(ValueError):
            proposals.create_proposal(self.vault, "t", proposals_dir="proposals")
        # Nothing was written into the escape target.
        self.assertEqual(list(self.outside.iterdir()), [])

    def test_unicode_and_special_chars_title(self):
        path = proposals.create_proposal(
            self.vault, "Reunião: Núcleo & Métricas (2026)!", "Synthetic body."
        )
        self.assertTrue(path.exists())
        self.assertEqual(path.parent.name, "proposals")
        # Slug is ascii/file-safe; original title is preserved in the content.
        self.assertRegex(path.name, r"^[0-9A-Za-z.\-]+\.md$")
        self.assertIn("Reunião: Núcleo & Métricas (2026)!", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
