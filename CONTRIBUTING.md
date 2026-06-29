# Contributing to Runa

Thanks for your interest. Runa is **Draft v0.1**, so the most useful
contributions are small, focused, and honest about scope.

Organization-wide defaults (templates, shared policies) live in
[`polaris-open/.github`](https://github.com/polaris-open/.github). This file
covers what is specific to Runa.

## Ground rules

- **Keep changes small.** Prefer one focused PR over a large one.
- **No new runtime dependencies in v0.1.** Standard library only (CLI uses
  `argparse`, tests use `unittest`). If you think a dependency is needed, open
  an issue first.
- **Match the principles.** See [docs/principles.md](docs/principles.md): local-first,
  proposal-first, append-first, explicit over magical.
- **Tests pass.** Run `make check` before opening a PR.

## Privacy and example content

Runa operates on personal/local knowledge, so privacy is part of the design.

- **Public examples must be synthetic.** Never add real data, secrets, tokens,
  credentials, corporate information, or PII to the repository.
- Do not commit anything copied from a real vault.
- See [docs/safety-and-privacy.md](docs/safety-and-privacy.md) and
  [SECURITY.md](SECURITY.md).

## Local setup

```bash
# Python >= 3.11, no install needed
make test     # run the unittest suite
make check    # tests + CLI smoke checks + compileall
make demo     # --help, doctor, scan on the example vault
```

## Suggesting larger ideas

Open an issue describing the problem before writing a large change. The
[ROADMAP.md](ROADMAP.md) shows the intended direction; proposals that fit it are
easier to land.
