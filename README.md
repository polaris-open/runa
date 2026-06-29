# Runa

> **Status: Draft v0.1 — early concept / runnable skeleton**

Local-first, Markdown-first operator for knowledge bases and project workflows.

> Runa is not a chatbot over notes.
> Runa is an operator for Markdown knowledge bases and project workflows.

---

## ⚠️ Read this first

This is an early skeleton. Specifically:

- **Runa is not production-ready.**
- **Runa does not call external LLMs yet.**
- **Runa does not implement RAG yet.**
- **Runa does not modify vault files silently.**
- **Public examples use synthetic content only.**
- **Do not test with private vaults before understanding the tool.**

If you want a finished local AI assistant today, this repository is not that
yet. If you want a small, honest, local-first foundation designed to grow into
one, you are in the right place.

## What it is

Runa is a tool/engine/CLI for operating Markdown vaults that are versioned in
Git and compatible with Obsidian — without depending on Obsidian. The long-term
goal is to help people:

- ask questions of their own vault;
- capture ideas quickly;
- track projects;
- generate change *proposals* instead of silent edits;
- organize personal work;
- work with configurable personas;
- integrate local LLMs or OpenAI-compatible providers **in the future**.

The goal of **this** first commit is much smaller: a clean, runnable skeleton
with an honest scope.

## What it is not

- Not a chatbot wrapped around your notes.
- Not a RAG system (no retrieval, no embeddings yet).
- Not connected to any LLM provider (OpenAI, Anthropic, Ollama — none).
- Not a cloud service, web UI, desktop app, or Obsidian plugin.
- Not an autonomous agent.

## Why it exists

Markdown vaults grow faster than they can be maintained. Notes pile up, projects
drift, and ideas get lost. The common "fix" is to point a chatbot at the folder,
but that hides what changed and why. Runa takes a different stance: knowledge
work should be **explicit, inspectable, and reversible**. When Runa wants to
change knowledge, it should create a **proposal** before touching source files.

> The default behavior should be local, explicit, inspectable, and reversible.

## Principles

Runa is designed to be:

- **Markdown-first** — plain `.md` files are the source of truth.
- **Git-first** — history and review come from version control.
- **Local-first** — everything runs on your machine by default.
- **Cloud-capable, not cloud-first** — the cloud is optional, never required.
- **Obsidian-compatible, not Obsidian-dependent** — works with Obsidian vaults, needs none of it.
- **LLM-neutral / provider-neutral** — no provider is special; none is bundled.
- **Proposal-first** — changes to knowledge are proposed, not silently applied.
- **Append-first** — `capture` only appends; it never rewrites.
- **Safety-first / privacy-aware** — your knowledge is personal; treat it that way.
- **Explicit over magical** — no hidden network calls, no surprise edits.

See [docs/principles.md](docs/principles.md) for the full discussion.

## Quick commands

```bash
make validate
make test
make check

PYTHONPATH=src python -m runa --help
PYTHONPATH=src python -m runa doctor --vault examples/vault-minimal
PYTHONPATH=src python -m runa scan --vault examples/vault-minimal
```

Requirements: Python >= 3.11. No third-party dependencies in v0.1.

For a guided 10–15 minute local test, follow:
[examples/vault-minimal/walkthrough.md](examples/vault-minimal/walkthrough.md)

## Example usage

Read-only inspection of the synthetic example vault:

```bash
PYTHONPATH=src python -m runa doctor --vault examples/vault-minimal
PYTHONPATH=src python -m runa scan  --vault examples/vault-minimal
```

Commands that write should run against a **temporary copy** so the versioned
example is never changed:

```bash
rm -rf /tmp/runa-vault-test
cp -R examples/vault-minimal /tmp/runa-vault-test

# Append-only capture into inbox.md
PYTHONPATH=src python -m runa capture --vault /tmp/runa-vault-test \
  --text "Synthetic test capture for Runa v0.1."

# Create a proposal without touching existing notes
PYTHONPATH=src python -m runa propose --vault /tmp/runa-vault-test \
  --title "Improve project status note" \
  --body "Synthetic proposal created during validation."
```

`ask` exists but fails honestly — Runa does not do retrieval or LLM calls yet:

```bash
PYTHONPATH=src python -m runa ask --vault examples/vault-minimal "What is this vault about?"
# -> `ask` is not implemented in v0.1. (exit code != 0)
```

## Roadmap (summary)

- **v0.1** — runnable skeleton: CLI, config, scan, capture, propose, example vault, tests.
- **v0.2** — local retrieval prototype (simple search; embeddings optional/local-only spike).
- **v0.3** — provider abstraction (local + OpenAI-compatible interfaces, privacy modes).
- **v0.4** — proposal workflows (review/apply flow, Git integration).
- **Future** — Ollama, embeddings, RAG, MCP, Obsidian plugin, web UI, cloud-capable mode.

Roadmap is not a promise. Full version in [ROADMAP.md](ROADMAP.md).

## Learn more

- [START_HERE.md](START_HERE.md) — pick the path that matches who you are.
- [docs/vision.md](docs/vision.md) — why Runa exists.
- [docs/principles.md](docs/principles.md) — the principles in detail.
- [docs/architecture.md](docs/architecture.md) — how it is put together.
- [docs/decisions/](docs/decisions/) — architecture decision records.
- [examples/vault-minimal/README.md](examples/vault-minimal/README.md) — the synthetic example vault.

## License

[Apache-2.0](LICENSE). Runa is an open source project of Polaris
([polaris-open](https://github.com/polaris-open)).
