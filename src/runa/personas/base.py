"""Conceptual persona shape.

A persona is configuration that shapes tone and behavior. It is NOT a hardcoded
character, and a persona never overrides safety rules. No specific persona is
defined in v0.1. See docs/personas.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Persona:
    """Behavioral configuration for how Runa communicates.

    Fields are descriptive only in v0.1; nothing consumes them yet.
    """

    name: str
    description: str = ""
    tone: str = "neutral"
    constraints: list[str] = field(default_factory=list)
