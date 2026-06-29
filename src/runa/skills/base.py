"""Conceptual skill shape.

A skill is a scoped, describable capability (for example: summarize a note,
draft a proposal). No real skill is implemented in v0.1; this only defines the
shape so future work has a place to land.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Skill:
    """Description of a scoped capability.

    Fields are descriptive only in v0.1; nothing executes them yet.
    """

    name: str
    description: str = ""
    required_context: list[str] = field(default_factory=list)
    safety_notes: list[str] = field(default_factory=list)
