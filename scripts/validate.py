#!/usr/bin/env python3
"""Local repository hygiene checks for Runa (standard library only).

What this is:
    A small, dependency-free script that checks the *structure* of the repo and
    a few honesty disclaimers, and greps for a short list of risky terms so a
    human can review them.

What this is NOT (be honest about the limits):
    - Not a security scanner, secret scanner, linter, or type checker.
    - It can miss real secrets and real PII. A clean run means "nothing obvious
      was found", never "this repo is safe".
    - It does not access the network, call any LLM, install anything, or modify
      files.

Exit codes:
    0  all hard checks passed (warnings may still be printed for human review)
    1  a hard check failed: a required file is missing/empty, pyproject metadata
       is wrong, a README disclaimer is missing, or an obvious real-secret
       pattern was found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

# --- Expected structure -----------------------------------------------------

REQUIRED_FILES = [
    "README.md",
    "START_HERE.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
    "ROADMAP.md",
    "pyproject.toml",
    "Makefile",
    ".gitignore",
    "runa.yaml.example",
    "docs/README.md",
    "docs/mvp.md",
]

EXAMPLE_VAULT_FILES = [
    "examples/vault-minimal/README.md",
    "examples/vault-minimal/runa.yaml",
    "examples/vault-minimal/inbox.md",
    "examples/vault-minimal/notes/ai-engineering.md",
    "examples/vault-minimal/projects/polaris.md",
    "examples/vault-minimal/proposals/README.md",
]

PACKAGE_FILES = [
    "src/runa/__init__.py",
    "src/runa/__main__.py",
    "src/runa/cli.py",
    "src/runa/vault.py",
    "src/runa/capture.py",
    "src/runa/proposals.py",
    "src/runa/safety.py",
]

TEST_FILES = [
    "tests/test_cli.py",
    "tests/test_config.py",
    "tests/test_vault.py",
    "tests/test_proposals.py",
    # Security/privacy baseline: these must not be removable without notice.
    "tests/test_dry_run.py",
    "tests/test_no_network.py",
    "tests/test_path_security.py",
    "tests/test_safety.py",
    "tests/test_static_no_network.py",
]

README_DISCLAIMERS = [
    "Draft v0.1",
    "not production-ready",
    "does not call external LLMs",
    "does not implement RAG",
    "synthetic content only",
]

# --- Term / secret scanning -------------------------------------------------

# Printed for HUMAN review only. Finding these is NOT a failure: they appear
# legitimately in safety docs and in "do not commit this" examples.
DANGEROUS_TERMS = [
    "api_key", "apikey", "secret", "token", "password", "passwd", "senha",
    "cpf", "cnpj", "credit card", "cartão", "telefone", "phone", "email",
    "customer", "cliente",
]
_TERM_RE = re.compile("|".join(re.escape(t) for t in DANGEROUS_TERMS), re.IGNORECASE)

# Obvious real-secret shapes. A match here IS a failure. Each pattern requires a
# realistic suffix so this file does not match its own pattern definitions.
SECRET_PATTERNS = [
    ("openai-style key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("github token", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("github PAT", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("aws access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private key block", re.compile(r"BEGIN [A-Z ]*PRIVATE KEY")),
]

TEXT_SUFFIXES = {
    ".md", ".py", ".toml", ".yml", ".yaml", ".cfg", ".ini", ".txt",
    ".example", ".editorconfig", ".gitignore",
}
TEXT_FILENAMES = {"Makefile", ".gitignore", ".editorconfig"}
SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "build", "dist",
    ".mypy_cache", ".pytest_cache", ".ruff_cache",
}


def _iter_text_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.name.endswith(".egg-info"):
            continue
        if path.suffix in TEXT_SUFFIXES or path.name in TEXT_FILENAMES:
            yield path


# --- Check runner -----------------------------------------------------------

class Checker:
    def __init__(self) -> None:
        self.failed = False

    def ok(self, message: str) -> None:
        print(f"OK: {message}")

    def warn(self, message: str) -> None:
        print(f"WARN: {message}")

    def fail(self, message: str) -> None:
        self.failed = True
        print(f"FAIL: {message}")


def _missing(rel_paths):
    return [p for p in rel_paths if not (ROOT / p).is_file()]


def _empty(rel_paths):
    return [
        p for p in rel_paths
        if (ROOT / p).is_file() and (ROOT / p).stat().st_size == 0
    ]


def check_required_files(c: Checker) -> None:
    missing = _missing(REQUIRED_FILES)
    if missing:
        c.fail(f"required files missing: {', '.join(missing)}")
    else:
        c.ok("required files exist.")


def check_required_not_empty(c: Checker) -> None:
    all_files = REQUIRED_FILES + EXAMPLE_VAULT_FILES + PACKAGE_FILES + TEST_FILES
    empty = _empty(all_files)
    if empty:
        c.fail(f"required files are empty: {', '.join(empty)}")
    else:
        c.ok("required files are not empty.")


def check_pyproject(c: Checker) -> None:
    path = ROOT / "pyproject.toml"
    if not path.is_file():
        c.fail("pyproject.toml is missing.")
        return
    text = path.read_text(encoding="utf-8")
    needles = [
        'name = "runa"',
        'requires-python = ">=3.11"',
        'runa = "runa.cli:main"',
    ]
    missing = [n for n in needles if n not in text]
    if missing:
        c.fail(f"pyproject.toml missing expected entries: {missing}")
    else:
        c.ok("pyproject metadata looks valid.")


def check_readme_disclaimers(c: Checker) -> None:
    path = ROOT / "README.md"
    if not path.is_file():
        c.fail("README.md is missing.")
        return
    text = path.read_text(encoding="utf-8")
    missing = [d for d in README_DISCLAIMERS if d not in text]
    if missing:
        c.fail(f"README missing safety disclaimers: {missing}")
    else:
        c.ok("README safety disclaimers found.")


def check_example_vault(c: Checker) -> None:
    missing = _missing(EXAMPLE_VAULT_FILES)
    if missing:
        c.fail(f"example vault files missing: {', '.join(missing)}")
    else:
        c.ok("example vault structure found.")


def check_package(c: Checker) -> None:
    missing = _missing(PACKAGE_FILES)
    if missing:
        c.fail(f"package files missing: {', '.join(missing)}")
    else:
        c.ok("Python package structure found.")


def check_tests(c: Checker) -> None:
    missing = _missing(TEST_FILES)
    if missing:
        c.fail(f"test files missing: {', '.join(missing)}")
    else:
        c.ok("tests found.")


def scan_dangerous_terms(c: Checker) -> None:
    """Print risky-term matches for human review. Never fails on its own."""
    matches: list[str] = []
    for path in _iter_text_files():
        if path.resolve() == SELF:
            continue  # avoid flagging this script's own term list
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(ROOT)
        for lineno, line in enumerate(lines, start=1):
            if _TERM_RE.search(line):
                matches.append(f"  {rel}:{lineno}: {line.strip()}")

    if matches:
        c.warn("dangerous-term scan found matches for human review.")
        print("\n".join(matches))
        print(
            "  (review only — these are expected in safety docs and "
            "'do not commit this' examples; not a failure.)"
        )
    else:
        c.ok("dangerous-term scan found no matches.")


def scan_real_secrets(c: Checker) -> None:
    """Fail if an obvious real-secret pattern is found."""
    hits: list[str] = []
    for path in _iter_text_files():
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(ROOT)
        for lineno, line in enumerate(lines, start=1):
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    hits.append(f"  {rel}:{lineno}: possible {label}")

    if hits:
        c.fail("obvious real-secret patterns found:")
        print("\n".join(hits))
    else:
        c.ok("no obvious real secret patterns found.")


def main() -> int:
    c = Checker()
    check_required_files(c)
    check_required_not_empty(c)
    check_pyproject(c)
    check_readme_disclaimers(c)
    check_example_vault(c)
    check_package(c)
    check_tests(c)
    scan_dangerous_terms(c)
    scan_real_secrets(c)

    if c.failed:
        print("FAIL: validation found problems (see above).")
        return 1
    c.ok("validation completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
