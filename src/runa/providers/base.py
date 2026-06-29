"""Conceptual provider interface.

This is a placeholder shape for future local and OpenAI-compatible providers.
No provider is enabled in v0.1, and there is no real implementation: calling
``generate`` raises ``NotImplementedError``.

Runa makes no external calls in v0.1.
"""

from __future__ import annotations


class Provider:
    """Abstract base for a text generation provider.

    Subclasses (added in later versions) will implement ``generate``. Privacy
    modes will decide whether a provider is even allowed to run. None of that
    exists yet.
    """

    name: str = "base"

    def generate(self, prompt: str) -> str:  # pragma: no cover - interface only
        """Return a completion for ``prompt``.

        Not implemented in v0.1. No provider is enabled and no external call is
        made by Runa.
        """
        raise NotImplementedError("No provider is enabled in v0.1.")
