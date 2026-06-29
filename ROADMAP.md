# Roadmap

> **Roadmap is not a promise.** It describes intended direction, not committed
> dates or features. Scope changes as the project learns.

## v0.1 — Runnable skeleton (current)

- Minimal CLI (`doctor`, `scan`, `capture`, `propose`, honest `ask`).
- Vault configuration file presence (`runa.yaml`), without full parsing.
- Read-only vault scan.
- Append-only `capture`.
- Proposal creation that never edits existing notes.
- Synthetic example vault.
- Tests, Makefile, local validations.

## v0.2 — Local search prototype

- Simple, deterministic local search over Markdown.
- File metadata extraction.
- Evidence-oriented search results.
- No LLM provider.
- No RAG.
- No embeddings yet — or at most an optional, local-only spike.

## v0.3 — Provider abstraction

- Local provider interface.
- OpenAI-compatible provider interface.
- Explicit privacy modes (what may leave the machine, and when).
- Still no provider bundled by default.

## v0.4 — Proposal workflows

- Richer proposal lifecycle (states beyond "proposed").
- Review / apply flow (apply is still human-gated).
- Git integration for proposals and applied changes.

## Future (unordered, not committed)

- Ollama and other local runtimes.
- Embeddings.
- RAG.
- MCP server.
- Obsidian plugin.
- Web UI.
- Cloud-capable mode.
- Rust core evaluation spike.
- Tauri desktop evaluation spike.

None of the "Future" items exist today, and listing them here is not a
commitment to build them.
