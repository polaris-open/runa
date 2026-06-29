"""Append-first capture into the vault inbox.

``capture`` is the one explicit exception to Runa's proposal-first rule: it is a
direct, append-only, reversible action. It NEVER rewrites the inbox; it only
appends a timestamped entry. If the inbox does not exist it is created with a
heading.

No network, no provider, no LLM.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from runa import safety
from runa.vault import resolve_vault

DEFAULT_INBOX = "inbox.md"


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def capture(
    vault_path: str | Path,
    text: str,
    inbox_name: str = DEFAULT_INBOX,
    dry_run: bool = False,
) -> Path:
    """Append ``text`` to the vault inbox as a timestamped entry.

    Returns the path of the inbox (the file that was, or would be, written).
    Raises ``ValueError`` if the text is empty or if the resolved inbox would
    fall outside the vault.

    When ``dry_run`` is true, the input and destination are still validated, but
    no file is created or modified.
    """
    vault = resolve_vault(vault_path)
    clean = safety.ensure_non_empty_text(text)

    inbox = safety.ensure_path_inside_vault(vault / inbox_name, vault)

    if dry_run:
        return inbox

    # Create with a heading on first use; otherwise append only.
    if not inbox.exists():
        inbox.write_text("# Inbox\n", encoding="utf-8")

    entry = f"\n- {_utc_timestamp()} {clean}\n"
    with inbox.open("a", encoding="utf-8") as handle:
        handle.write(entry)

    return inbox
