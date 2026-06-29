"""Provider abstractions (conceptual only in v0.1).

Runa is provider-neutral and LLM-neutral. No provider is enabled in v0.1 and
nothing here makes external calls. See docs/providers.md.
"""

from runa.providers.base import Provider

__all__ = ["Provider"]
