# Terminology

Shared vocabulary for Runa. Some terms describe things that exist in v0.1;
others describe concepts the design reserves space for.

- **Vault** — a directory of plain Markdown files, usually versioned in Git and
  often Obsidian-compatible. The unit Runa operates on.
- **Inbox** — a single Markdown file (default `inbox.md`) that `capture` appends
  to. The fast, low-friction entry point for ideas.
- **Proposal** — a Markdown file describing a suggested change, created under
  `proposals/`. It never edits source notes. There is no automatic apply in v0.1.
- **Provider** — an abstraction over a text-generation backend (local or
  OpenAI-compatible). **No provider is enabled in v0.1.**
- **Persona** — configuration that shapes tone and behavior. Not a hardcoded
  character, and never a replacement for safety rules. None ship in v0.1.
- **Skill** — a scoped, describable capability Runa may gain later. Only a
  conceptual shape exists in v0.1.
- **Agent** — an actor that can plan and take actions. **The Runa v0.1 skeleton
  does not implement autonomous agents.** The word "agent" in the tagline
  describes the long-term aim, not current behavior.
- **Local-first** — runs entirely on your machine by default; no network needed.
- **Cloud-capable** — able to use optional cloud features later, never required to.
- **Markdown-first** — plain `.md` files are the source of truth.
- **Git-first** — history and review come from version control.
- **Apply** — the (future) act of turning a proposal into an actual change to
  source notes. **Not implemented in v0.1.**
- **Capture** — the append-only action of adding a timestamped entry to the inbox.
