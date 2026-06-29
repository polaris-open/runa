# Start here

Runa is **Draft v0.1 — early concept / runnable skeleton**. Pick the profile
that matches you, then follow *read first / do first / avoid / first artifact*.

Honest summary up front:

- If you want a ready-made **LLM/RAG** assistant — it does not exist yet.
- If you want an **Obsidian plugin** — it does not exist yet.
- If you want **cloud sync** — it does not exist yet.
- If you want a small, honest **local-first foundation** to grow — this is the right place.

---

## I want to evaluate Runa in 10 minutes

- **Read first:** [examples/vault-minimal/walkthrough.md](examples/vault-minimal/walkthrough.md).
- **Do first:** run `make check`, then follow the walkthrough against the synthetic vault.
- **Avoid:** using your real/private vault.
- **First artifact:** a temporary inbox entry and proposal generated under `/tmp/runa-vault-test`.

## I just want to understand Runa

- **Read first:** [README.md](README.md), then [docs/vision.md](docs/vision.md) and [docs/principles.md](docs/principles.md).
- **Do first:** nothing to install. Skim [docs/terminology.md](docs/terminology.md).
- **Avoid:** assuming there is a working AI behind it. There isn't, yet.
- **First artifact:** a clear mental model of "operator for Markdown vaults, not a chatbot."

## I want to run the CLI

- **Read first:** the "Quick commands" section of [README.md](README.md).
- **Do first:**
  ```bash
  make test
  PYTHONPATH=src python -m runa doctor --vault examples/vault-minimal
  PYTHONPATH=src python -m runa scan  --vault examples/vault-minimal
  ```
- **Avoid:** running write commands against a vault you care about. Use a copy.
- **First artifact:** a passing `make test` and a successful `scan` on the example vault.

## I use Obsidian

- **Read first:** [docs/vault-contract.md](docs/vault-contract.md).
- **Do first:** point `scan` at a **copy** of a small, non-sensitive vault.
- **Avoid:** pointing Runa at your real vault before you trust it. There is no Obsidian plugin and Runa does not need `.obsidian/` (it is ignored).
- **First artifact:** a scan count of a copied vault, confirming Runa reads plain Markdown.

## I want a local AI assistant

- **Read first:** [docs/providers.md](docs/providers.md) and [docs/safety-and-privacy.md](docs/safety-and-privacy.md).
- **Do first:** set expectations — `ask` intentionally fails in v0.1.
- **Avoid:** expecting answers from your notes today. No retrieval, no LLM.
- **First artifact:** an understanding of the provider-neutral plan (v0.3+).

## I want to contribute

- **Read first:** [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/architecture.md](docs/architecture.md).
- **Do first:** `make check`, then read [docs/mvp.md](docs/mvp.md) for what "done" means in v0.1.
- **Avoid:** large PRs and new dependencies. v0.1 is standard-library only.
- **First artifact:** a small, focused change with tests that still pass `make check`.

## I want to build providers later

- **Read first:** [docs/providers.md](docs/providers.md) and `src/runa/providers/base.py`.
- **Do first:** read the `Provider` shape; note that no provider is enabled in v0.1.
- **Avoid:** wiring real API calls now. Provider work lands in v0.3.
- **First artifact:** notes on the interface you would need for a local or OpenAI-compatible provider.

## I want to use Runa for personal project management

- **Read first:** [examples/vault-minimal/projects/polaris.md](examples/vault-minimal/projects/polaris.md).
- **Do first:** try `capture` and `propose` on a copied vault.
- **Avoid:** treating proposals as auto-applied changes. There is no apply step yet.
- **First artifact:** an inbox entry and a generated proposal file you reviewed by hand.
