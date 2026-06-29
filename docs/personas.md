# Personas

A **persona** is configuration that shapes *how* Runa communicates — tone, style,
constraints — not a character with a backstory.

## Personas are configuration, not characters

- A persona is data: a name, a description, a tone, and a list of constraints
  (see the `Persona` shape in `src/runa/personas/base.py`).
- Personas should be **configurable**, living in a vault's config rather than
  hardcoded into Runa.
- No specific persona ships with Runa in v0.1.

## No hardcoded characters

Runa does **not** ship "Merlin", "Gandalf", "Athena", or any other named
character as a default. Such names are, at most, *examples* a user could define
themselves in the future — never built-in defaults, and never required.

## Personas never override safety

A persona can change tone; it can never change the rules. Safety and privacy
behavior (proposal-first, append-first, staying inside the vault, no silent
edits) sit **below** personas and are not negotiable by them. A persona that
"wants" to bypass a safety rule is simply ignored on that point.

## Status in v0.1

- The `Persona` dataclass exists as a conceptual shape only.
- Nothing consumes personas yet — there is no generation in v0.1.
- The example config uses `persona.default: "neutral"` as a placeholder.

See [principles.md](principles.md) and
[safety-and-privacy.md](safety-and-privacy.md).
