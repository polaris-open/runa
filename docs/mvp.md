# MVP — v0.1 scope

The v0.1 MVP is a **runnable skeleton**: a small, honest foundation that works
and can be trusted, not a feature-complete product.

## What exists now

- A CLI (`python -m runa`) built on `argparse`, standard library only.
- `doctor` — checks that a vault looks usable (no network, no LLM).
- `scan` — counts Markdown files, read-only.
- `capture` — append-only entry into the inbox.
- `propose` — creates a proposal file without editing existing notes.
- `ask` — present but intentionally failing (honest about the missing AI).
- Minimal config discovery (`runa.yaml` presence; no full parsing).
- A synthetic example vault.
- A `unittest` suite, a `Makefile`, and local validation commands.

## What does NOT exist now

- No retrieval (RAG), no embeddings.
- No LLM provider, no external calls (OpenAI, Anthropic, Ollama — none).
- No apply step for proposals.
- No full YAML parsing.
- No MCP server, web UI, desktop app, Obsidian plugin, cloud, auth, or database.
- No autonomous agent.

## How to validate

```bash
make test
make check
make demo

PYTHONPATH=src python -m runa --help
PYTHONPATH=src python -m runa doctor --vault examples/vault-minimal
PYTHONPATH=src python -m runa scan  --vault examples/vault-minimal
```

Write commands should run against a temporary copy:

```bash
rm -rf /tmp/runa-vault-test
cp -R examples/vault-minimal /tmp/runa-vault-test
PYTHONPATH=src python -m runa capture --vault /tmp/runa-vault-test --text "Synthetic capture."
PYTHONPATH=src python -m runa propose --vault /tmp/runa-vault-test --title "Synthetic proposal"
```

## Definition of done for v0.1

- `make check` passes (tests + CLI smoke checks + `compileall`).
- `scan` makes no network calls and respects ignored directories.
- `capture` only appends; it never rewrites a file.
- `propose` creates a file and never modifies existing notes.
- `ask` exits non-zero with an honest message.
- The repository contains no secrets, no PII, and only synthetic examples.
- The README is honest that this is Draft v0.1.
