"""Vault discovery and read-only scanning.

A "vault" is a directory of plain Markdown files (Obsidian-compatible, but not
Obsidian-dependent). Everything here is read-only and local. No network, no
provider, no LLM.
"""

from __future__ import annotations

import os
from pathlib import Path

# Directories that are never part of the knowledge content we scan.
IGNORED_DIRS: frozenset[str] = frozenset(
    {".git", ".obsidian", "proposals", "__pycache__", ".venv"}
)


def resolve_vault(path: str | Path) -> Path:
    """Resolve ``path`` to an existing vault directory.

    Raises ``FileNotFoundError`` if it does not exist and ``NotADirectoryError``
    if it is not a directory.
    """
    vault = Path(path).expanduser().resolve()
    if not vault.exists():
        raise FileNotFoundError(f"Vault path does not exist: {vault}")
    if not vault.is_dir():
        raise NotADirectoryError(f"Vault path is not a directory: {vault}")
    return vault


def list_markdown_files(path: str | Path) -> list[Path]:
    """Return a sorted list of Markdown files in the vault.

    Ignores ``.git``, ``.obsidian``, ``proposals``, ``__pycache__`` and
    ``.venv`` at any depth.
    """
    vault = resolve_vault(path)
    found: list[Path] = []
    for root, dirs, files in os.walk(vault):
        # Prune ignored directories in place so os.walk does not descend.
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for name in files:
            if name.endswith(".md"):
                found.append(Path(root) / name)
    return sorted(found)


def top_level_directories(path: str | Path) -> list[Path]:
    """Return the non-ignored top-level directories of the vault, sorted."""
    vault = resolve_vault(path)
    return sorted(
        (p for p in vault.iterdir() if p.is_dir() and p.name not in IGNORED_DIRS),
        key=lambda p: p.name,
    )


def scan_vault(path: str | Path) -> dict:
    """Return a read-only summary of the vault.

    The returned dict contains the resolved vault path, the count of Markdown
    files, the top-level directory names and the relative file paths. No content
    leaves the machine.
    """
    vault = resolve_vault(path)
    markdown_files = list_markdown_files(vault)
    return {
        "vault": str(vault),
        "markdown_files": len(markdown_files),
        "top_level_directories": [d.name for d in top_level_directories(vault)],
        "files": [str(p.relative_to(vault)) for p in markdown_files],
    }
