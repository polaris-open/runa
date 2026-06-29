"""Proposal creation.

Proposal-first: when Runa wants to change knowledge, it writes a proposal
instead of editing source notes. In v0.1 a proposal is just a Markdown file
under ``proposals/``. It NEVER touches existing notes, and there is no automatic
apply step yet (see docs/proposals.md).

No network, no provider, no LLM.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from runa import safety
from runa.vault import resolve_vault

DEFAULT_PROPOSALS_DIR = "proposals"

_SAFETY_NOTE = (
    "This proposal was created by Runa and applies nothing automatically. "
    "Review it manually before changing any source note. Runa v0.1 has no apply step."
)


def slugify(title: str) -> str:
    """Turn a title into a simple, file-safe slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "proposal"


def _render(title: str, body: str, created_at: str) -> str:
    body_text = body.strip() if body and body.strip() else "_No body provided._"
    return (
        f"# {title}\n\n"
        f"- **Status:** proposed\n"
        f"- **Created at:** {created_at}\n\n"
        f"## Summary\n\n"
        f"{body_text}\n\n"
        f"## Safety note\n\n"
        f"{_SAFETY_NOTE}\n"
    )


def create_proposal(
    vault_path: str | Path,
    title: str,
    body: str = "",
    proposals_dir: str = DEFAULT_PROPOSALS_DIR,
) -> Path:
    """Create a new proposal Markdown file under ``proposals/``.

    Returns the path of the created file. The file name is
    ``<UTC timestamp>-<slug>.md``. Raises ``ValueError`` if the title is empty or
    if the resolved path would fall outside the vault.

    Existing notes are never modified.
    """
    vault = resolve_vault(vault_path)
    clean_title = safety.ensure_non_empty_text(title)

    proposals = vault / proposals_dir
    proposals.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    created_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    slug = slugify(clean_title)

    # Avoid clobbering an existing proposal created in the same second.
    candidate = proposals / f"{stamp}-{slug}.md"
    counter = 1
    while candidate.exists():
        candidate = proposals / f"{stamp}-{slug}-{counter}.md"
        counter += 1

    path = safety.ensure_path_inside_vault(candidate, vault)
    path.write_text(_render(clean_title, body, created_at), encoding="utf-8")
    return path
