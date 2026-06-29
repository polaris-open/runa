"""Static guard: src/runa must not import network/exec modules or call exec-y APIs.

This complements the runtime ``test_no_network`` monkeypatch guardrail with a
cheap static check over the package source. It is NOT a full policy engine; it
catches the obvious regressions (importing ``socket``/``urllib``/``subprocess``,
calling ``os.system``/``eval``/``__import__``, etc.) before they ship.

It scans only ``src/runa`` (the shipped package), not the tests themselves.
"""

import ast
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

SRC = Path(__file__).resolve().parents[1] / "src" / "runa"

# Top-level module names that have no business in a local-only v0.1 package.
FORBIDDEN_IMPORTS = {
    "socket", "ssl", "urllib", "http", "ftplib", "smtplib", "poplib",
    "imaplib", "telnetlib", "nntplib", "xmlrpc", "asyncio",
    "requests", "httpx", "aiohttp", "urllib3",
    "subprocess", "importlib",
}
# Direct builtin calls that enable dynamic execution.
FORBIDDEN_CALL_NAMES = {"eval", "exec", "__import__"}
# os.<attr> prefixes that shell out or exec.
FORBIDDEN_OS_ATTR_PREFIXES = ("system", "popen", "exec", "spawn")


def _top(module: str | None) -> str:
    return (module or "").split(".", 1)[0]


def _python_files():
    return sorted(SRC.rglob("*.py"))


class StaticNoNetworkTest(unittest.TestCase):
    def test_no_forbidden_imports(self):
        offenders = []
        for path in _python_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if _top(alias.name) in FORBIDDEN_IMPORTS:
                            offenders.append(f"{path.name}: import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.level == 0 and _top(node.module) in FORBIDDEN_IMPORTS:
                        offenders.append(f"{path.name}: from {node.module} import ...")
        self.assertEqual(offenders, [], f"forbidden imports in src/runa: {offenders}")

    def test_no_dynamic_exec_or_shell_calls(self):
        offenders = []
        for path in _python_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                func = node.func
                if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALL_NAMES:
                    offenders.append(f"{path.name}: {func.id}(...)")
                elif (
                    isinstance(func, ast.Attribute)
                    and isinstance(func.value, ast.Name)
                    and func.value.id == "os"
                    and func.attr.startswith(FORBIDDEN_OS_ATTR_PREFIXES)
                ):
                    offenders.append(f"{path.name}: os.{func.attr}(...)")
        self.assertEqual(offenders, [], f"dangerous calls in src/runa: {offenders}")


if __name__ == "__main__":
    unittest.main()
