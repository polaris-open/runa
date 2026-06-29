"""Small, explicit safety helpers.

Runa is safety-first. These helpers are intentionally simple. They are NOT a
security boundary and NOT a sophisticated PII/secret detector. They exist to
catch obvious mistakes and to keep write operations inside the vault.

Nothing here calls the network or any provider.
"""

from __future__ import annotations

import re
from pathlib import Path

# Very simple, obvious patterns. This is a hint, not a guarantee.
_SENSITIVE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("api_key", re.compile(r"api[\s_-]?key", re.IGNORECASE)),
    ("password", re.compile(r"password|passwd|senha", re.IGNORECASE)),
    ("secret", re.compile(r"secret", re.IGNORECASE)),
    ("token", re.compile(r"\btoken\b", re.IGNORECASE)),
    ("cpf", re.compile(r"\bcpf\b", re.IGNORECASE)),
    ("credit_card", re.compile(r"credit\s*card|cart[aã]o\s*de\s*cr[eé]dito", re.IGNORECASE)),
]


def ensure_non_empty_text(text: str | None) -> str:
    """Return ``text`` stripped, or raise ``ValueError`` if it is empty.

    Used by ``capture`` and ``propose`` so that empty input never produces a
    silent or meaningless write.
    """
    if text is None or not text.strip():
        raise ValueError("Text must not be empty.")
    return text.strip()


def ensure_path_inside_vault(path: str | Path, vault: str | Path) -> Path:
    """Return the fully resolved ``path`` if it lives inside ``vault``.

    Both the vault and the target are resolved with ``Path.resolve()``, which
    follows symlinks and collapses ``..`` segments. As a result this rejects, by
    raising ``ValueError``:

    - path traversal via ``..`` (e.g. ``vault/../secret``);
    - absolute paths pointing outside the vault (e.g. ``/etc/passwd``);
    - symlinks (file or directory) whose real target is outside the vault.

    The vault root itself is allowed (so the vault directory can be operated on),
    but everything written must be the vault or a descendant of it.
    """
    vault_resolved = Path(vault).expanduser().resolve()
    target = Path(path).expanduser().resolve()
    if target != vault_resolved and vault_resolved not in target.parents:
        raise ValueError(
            f"Refusing to operate outside the vault: {target} is not inside {vault_resolved}"
        )
    return target


def looks_sensitive(text: str | None) -> list[str]:
    """Return the names of obvious sensitive patterns found in ``text``.

    This is a best-effort hint only. An empty list means "nothing obvious was
    found", NOT "this text is safe". Runa never blocks on this; callers may warn
    the user.
    """
    if not text:
        return []
    found: list[str] = []
    for name, pattern in _SENSITIVE_PATTERNS:
        if pattern.search(text):
            found.append(name)
    return found
