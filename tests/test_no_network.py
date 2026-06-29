"""Guardrail tests: the main CLI commands must not attempt any network access.

These do not build a perfect sandbox. They monkeypatch the standard-library
socket entry points so that *any* attempt to open a connection raises. Each main
command is then run in-process under that block. If a command ever tries to use
the network, the patched functions raise and the test fails — catching an
accidental regression before Runa grows providers/RAG.
"""

import contextlib
import io
import shutil
import socket
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from runa import cli  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_VAULT = ROOT / "examples" / "vault-minimal"


class _NetworkAttempted(RuntimeError):
    pass


@contextlib.contextmanager
def block_network():
    """Replace socket entry points so any connection attempt raises."""
    saved_socket = socket.socket
    saved_create_connection = socket.create_connection
    saved_getaddrinfo = socket.getaddrinfo

    def _deny(*args, **kwargs):
        raise _NetworkAttempted("network access attempted; forbidden in Runa v0.1")

    socket.socket = _deny
    socket.create_connection = _deny
    socket.getaddrinfo = _deny
    try:
        yield
    finally:
        socket.socket = saved_socket
        socket.create_connection = saved_create_connection
        socket.getaddrinfo = saved_getaddrinfo


def run_cli(*args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return cli.main(list(args))


class NoNetworkTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name) / "vault"
        shutil.copytree(EXAMPLE_VAULT, self.vault)

    def tearDown(self):
        self._tmp.cleanup()

    def test_doctor_no_network(self):
        with block_network():
            self.assertEqual(run_cli("doctor", "--vault", str(self.vault)), 0)

    def test_scan_no_network(self):
        with block_network():
            self.assertEqual(run_cli("scan", "--vault", str(self.vault)), 0)

    def test_capture_no_network(self):
        with block_network():
            self.assertEqual(
                run_cli("capture", "--vault", str(self.vault), "--text", "synthetic"), 0
            )

    def test_propose_no_network(self):
        with block_network():
            self.assertEqual(
                run_cli("propose", "--vault", str(self.vault), "--title", "synthetic"), 0
            )

    def test_ask_no_network(self):
        # ask fails honestly (exit 2) and must not touch the network either.
        with block_network():
            self.assertEqual(run_cli("ask", "--vault", str(self.vault), "anything"), 2)

    def test_block_actually_blocks(self):
        # Sanity check: the guard really does prevent opening a socket.
        with block_network():
            with self.assertRaises(_NetworkAttempted):
                socket.socket()


if __name__ == "__main__":
    unittest.main()
