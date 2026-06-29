"""Configuration discovery for a vault.

A vault MAY contain a ``runa.yaml`` file. In this v0.1 skeleton we do NOT depend
on PyYAML or any external dependency, so we do not parse YAML into structured
config yet.

Full YAML parsing will be added later (see docs/configuration.md). For now these
helpers only locate the config file and expose its raw text, which is enough for
``doctor`` to report whether configuration is present.
"""

from __future__ import annotations

from pathlib import Path

CONFIG_FILENAME = "runa.yaml"


def find_config(vault_path: str | Path) -> Path | None:
    """Return the path to ``runa.yaml`` in the vault, or ``None`` if absent."""
    vault = Path(vault_path).expanduser().resolve()
    candidate = vault / CONFIG_FILENAME
    return candidate if candidate.is_file() else None


def load_config(vault_path: str | Path) -> dict:
    """Return a minimal description of the vault configuration.

    NOTE: Full YAML parsing is not implemented in the v0.1 skeleton. This returns
    a small dict so callers can reason about presence without a YAML dependency::

        {"exists": bool, "path": str | None, "raw": str | None}

    The ``raw`` field holds the file's text (when present) for display only; it is
    intentionally not interpreted.
    """
    config_path = find_config(vault_path)
    if config_path is None:
        return {"exists": False, "path": None, "raw": None}
    return {
        "exists": True,
        "path": str(config_path),
        "raw": config_path.read_text(encoding="utf-8"),
    }
