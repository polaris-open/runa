"""Tests for the Runa CLI.

These run the real CLI through ``python -m runa`` in a subprocess so the entry
point and exit codes are exercised end to end. Writing commands (capture,
propose) run against a temporary copy of the example vault so the versioned
example is never touched.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
EXAMPLE_VAULT = ROOT / "examples" / "vault-minimal"


def run_cli(*args):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC)
    return subprocess.run(
        [sys.executable, "-m", "runa", *args],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )


class CliTest(unittest.TestCase):
    def test_help(self):
        result = run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("runa", result.stdout.lower())

    def test_no_args_prints_help(self):
        result = run_cli()
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage", result.stdout.lower())

    def test_doctor_on_example_vault(self):
        result = run_cli("doctor", "--vault", str(EXAMPLE_VAULT))
        self.assertEqual(result.returncode, 0)
        self.assertIn("runa.yaml present: True", result.stdout)

    def test_scan_on_example_vault(self):
        result = run_cli("scan", "--vault", str(EXAMPLE_VAULT))
        self.assertEqual(result.returncode, 0)
        self.assertIn("Markdown files:", result.stdout)
        self.assertIn("No content was sent to any external provider", result.stdout)

    def test_ask_fails_honestly(self):
        result = run_cli("ask", "--vault", str(EXAMPLE_VAULT), "What is this vault about?")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not implemented in v0.1", result.stderr)

    def test_capture_and_propose_on_temp_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            shutil.copytree(EXAMPLE_VAULT, vault)

            cap = run_cli("capture", "--vault", str(vault), "--text", "Synthetic capture.")
            self.assertEqual(cap.returncode, 0)
            self.assertIn("Synthetic capture.", (vault / "inbox.md").read_text(encoding="utf-8"))

            prop = run_cli("propose", "--vault", str(vault), "--title", "Synthetic proposal")
            self.assertEqual(prop.returncode, 0)
            created = list((vault / "proposals").glob("*-synthetic-proposal.md"))
            self.assertEqual(len(created), 1)

    def test_capture_rejects_empty_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            shutil.copytree(EXAMPLE_VAULT, vault)
            result = run_cli("capture", "--vault", str(vault), "--text", "   ")
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
