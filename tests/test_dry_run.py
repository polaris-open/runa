"""Dry-run tests: write commands must not create or modify files."""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from runa import cli  # noqa: E402


def run_cli(*args):
    """Run the CLI in-process, swallowing stdout/stderr, return the exit code."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return cli.main(list(args))


class DryRunTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_capture_dry_run_creates_no_inbox(self):
        rc = run_cli("capture", "--vault", str(self.vault), "--text", "hello", "--dry-run")
        self.assertEqual(rc, 0)
        self.assertFalse((self.vault / "inbox.md").exists())

    def test_capture_dry_run_does_not_modify_existing_inbox(self):
        inbox = self.vault / "inbox.md"
        inbox.write_text("# Inbox\n\n- existing entry\n", encoding="utf-8")
        before = inbox.read_text(encoding="utf-8")
        rc = run_cli("capture", "--vault", str(self.vault), "--text", "new", "--dry-run")
        self.assertEqual(rc, 0)
        self.assertEqual(inbox.read_text(encoding="utf-8"), before)

    def test_propose_dry_run_creates_nothing(self):
        rc = run_cli("propose", "--vault", str(self.vault), "--title", "T", "--dry-run")
        self.assertEqual(rc, 0)
        # The proposals directory must not even be created in dry-run.
        self.assertFalse((self.vault / "proposals").exists())

    def test_capture_without_dry_run_still_writes(self):
        rc = run_cli("capture", "--vault", str(self.vault), "--text", "real entry")
        self.assertEqual(rc, 0)
        self.assertTrue((self.vault / "inbox.md").exists())
        self.assertIn("real entry", (self.vault / "inbox.md").read_text(encoding="utf-8"))

    def test_propose_without_dry_run_still_writes(self):
        rc = run_cli("propose", "--vault", str(self.vault), "--title", "Real proposal")
        self.assertEqual(rc, 0)
        created = list((self.vault / "proposals").glob("*.md"))
        self.assertEqual(len(created), 1)


if __name__ == "__main__":
    unittest.main()
