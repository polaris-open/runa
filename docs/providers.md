# Providers

Runa is **provider-neutral** and **LLM-neutral**. A "provider" is an abstraction
over a text-generation backend.

## v0.1: no provider

- **No provider is enabled in v0.1.**
- **No external calls are made by default — or at all — in v0.1.**
- `src/runa/providers/base.py` defines only a conceptual `Provider` shape whose
  `generate()` raises `NotImplementedError`.

This is intentional. Runa should be useful and trustworthy *before* any model is
involved.

## Planned interfaces (not built)

See [../ROADMAP.md](../ROADMAP.md), v0.3:

- **Local provider interface** — for a model running on your machine.
- **OpenAI-compatible provider interface** — for any endpoint that speaks the
  OpenAI-compatible API shape (self-hosted or remote).

No provider will be bundled or privileged. Choosing one will always be the user's
explicit decision.

## Privacy modes (planned)

When providers arrive, privacy modes will decide what — if anything — may leave
the machine:

- `local-first` (default) — keep everything local; do not call external
  providers.
- explicit opt-in modes — only with clear user consent, and ideally with
  redaction before anything is sent.

Until those modes exist and you have configured them, assume Runa sends nothing
anywhere. In v0.1 that is guaranteed: there is no provider and no network code.

See [safety-and-privacy.md](safety-and-privacy.md) for the broader stance.
