# Architecture

Runa v0.1 is deliberately small. The architecture below names the layers so
future work has obvious places to land — but most layers are thin or conceptual
today.

## Layers

```text
            +-----------------------------+
            |            CLI              |  argparse entry point (cli.py)
            +-----------------------------+
                          |
            +-----------------------------+
            |            Core             |  command wiring, exit codes
            +-----------------------------+
              |        |         |       |
   +----------+   +----+----+  +-+------+ +--------+
   |  Vault   |   |Proposals|  |Capture | | Safety |
   | (read)   |   | (write) |  |(append)| | (guard)|
   +----------+   +---------+  +--------+ +--------+
              \        |          /
            +-----------------------------+
            |  Providers / Personas /     |  conceptual shapes only in v0.1
            |  Skills (not enabled yet)   |
            +-----------------------------+
```

- **CLI** (`src/runa/cli.py`) — parses arguments with `argparse`, dispatches to
  commands, returns honest exit codes. No network, no LLM.
- **Core** — the command functions themselves; thin glue in v0.1.
- **Vault** (`src/runa/vault.py`) — resolve a vault path, list Markdown files,
  produce a read-only scan summary.
- **Proposals** (`src/runa/proposals.py`) — create proposal files; never touch
  existing notes.
- **Capture** (`src/runa/capture.py`) — append-only writes to the inbox.
- **Safety** (`src/runa/safety.py`) — small guards: non-empty text, stay inside
  the vault, hint at obviously sensitive strings.
- **Providers / Personas / Skills** — conceptual interfaces only. Nothing is
  enabled or executed in v0.1.

## Flow

- **scan** — `resolve vault → walk files (skip .git/.obsidian/proposals) → count
  → print summary`. Read-only; nothing leaves the machine.
- **capture** — `validate text → resolve inbox inside vault → append timestamped
  entry`. Additive and reversible.
- **propose** — `validate title → ensure proposals/ → write new file`. Existing
  notes are untouched; there is no apply step.
- **ask (future)** — would be `retrieve relevant notes → ask a provider →
  propose an answer/change`. **None of this exists in v0.1**, which is why `ask`
  fails honestly.

## Why so thin

The goal of v0.1 is a trustworthy skeleton, not a feature set. Keeping each layer
minimal makes the principles in [principles.md](principles.md) easy to verify and
the code easy to extend toward the [ROADMAP.md](../ROADMAP.md).

## Technology direction

Runa v0.1 is implemented in Python with the standard library only. This is a
deliberate choice to keep the skeleton easy to inspect, test, and change while
the core domain is still being validated.

Rust and Tauri are possible future directions for a product-grade local core and
desktop experience, but they are not part of v0.1 and should not be introduced
before local search, proposal workflows, and safety boundaries are validated.

See:

- [ADR 0002 — Operator, not agent](decisions/0002-operator-not-agent.md)
- [ADR 0003 — Python now, Rust/Tauri later](decisions/0003-python-now-rust-tauri-later.md)
