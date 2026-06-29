"""Small, explicit safety helpers.

Runa is safety-first. These helpers are intentionally simple. They are NOT a
security boundary and NOT a sophisticated PII/secret detector. They exist to
catch obvious mistakes and to keep write operations inside the vault.

Nothing here calls the network or any provider.
"""

from __future__ import annotations

import re
from pathlib import Path

# Very simple, obvious patterns grouped by category. This is a hint, not a
# guarantee and NOT a complete scanner: it will miss things and may over-match.
# Categories: secrets, credentials, pii, financial.
_SENSITIVE_PATTERNS: dict[str, list[tuple[str, re.Pattern[str]]]] = {
    "secrets": [
        ("secret", re.compile(r"secret", re.IGNORECASE)),
        ("private_key_block", re.compile(r"BEGIN [A-Z ]*PRIVATE KEY")),
    ],
    "credentials": [
        ("api_key", re.compile(r"api[\s_-]?key", re.IGNORECASE)),
        ("password", re.compile(r"password|passwd|senha", re.IGNORECASE)),
        ("token", re.compile(r"\btoken\b", re.IGNORECASE)),
        ("openai_key", re.compile(r"sk-[A-Za-z0-9]{16,}")),
        ("github_token", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
        ("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
        ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ],
    "pii": [
        ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
        ("cpf", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
        ("cpf_keyword", re.compile(r"\bcpf\b", re.IGNORECASE)),
        ("cnpj", re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")),
        ("br_phone", re.compile(r"\b(?:\+55\s?)?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}\b")),
    ],
    "financial": [
        ("credit_card_number", re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b")),
        ("credit_card_keyword", re.compile(r"credit\s*card|cart[aã]o\s*de\s*cr[eé]dito", re.IGNORECASE)),
    ],
}


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


def categorize_sensitive(text: str | None) -> dict[str, list[str]]:
    """Return obvious sensitive matches in ``text`` grouped by category.

    The result maps a category (``secrets``, ``credentials``, ``pii``,
    ``financial``) to the labels that matched. An empty dict means "nothing
    obvious was found", which is NOT the same as "this text is safe".

    This is a best-effort hint only — not a security boundary and not a complete
    secret/PII scanner. Runa never blocks on it; callers may warn the user.
    """
    result: dict[str, list[str]] = {}
    if not text:
        return result
    for category, patterns in _SENSITIVE_PATTERNS.items():
        hits = [name for name, pattern in patterns if pattern.search(text)]
        if hits:
            result[category] = hits
    return result


def looks_sensitive(text: str | None) -> list[str]:
    """Return a flat list of obvious sensitive labels found in ``text``.

    Convenience wrapper over :func:`categorize_sensitive`. Same caveats apply:
    an empty list does not mean the text is safe.
    """
    found: list[str] = []
    for hits in categorize_sensitive(text).values():
        found.extend(hits)
    return found
