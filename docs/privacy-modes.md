# Privacy modes

This document defines Runa's intended **privacy modes**. Most of it describes
*future* behavior. It is written now so the design constraints are explicit
before any provider, RAG, or external integration is built.

> **What is true today (v0.1):** Runa makes **no network calls** and has **no
> providers**. The effective behavior is `local-only`, enforced by the simple
> fact that there is no code that talks to anything off your machine. Everything
> below about external modes is **planned**, not implemented.

## The modes

| Mode | Meaning | Status |
|------|---------|--------|
| `local-only` | Nothing leaves the machine. No provider is contacted. | **Effective today** (by absence of any network code) |
| `local-redacted` | Local processing only, with redaction applied to any text before it is shown to a future local model. | Planned |
| `external-explicit` | A future external/OpenAI-compatible provider may be used, but only with explicit, per-action opt-in and a preview of exactly what would be sent. | Planned |
| `external-disabled` | External providers are hard-disabled regardless of other configuration — a safe default and a "kill switch". | Planned |

The intended default, now and later, is the most private mode that still does
the job — never a cloud-first default.

## Requirements for any future external send

If Runa ever sends vault content to a provider, that path **must** satisfy all of
the following before it ships:

- **Explicit opt-in.** No external send happens without a deliberate user action;
  there is no implicit or "smart" default that enables it.
- **Context preview.** The user can see exactly what text would be sent, before
  it is sent.
- **Redaction before send.** Obvious secrets/PII are redacted from the context
  first (and the redaction is inspectable). The current `safety` hints are a
  starting point, not the final redactor.
- **Allowlist of files/directories.** Only explicitly allowed paths can ever be
  included in an external context; everything else is excluded by default.
- **Local audit log.** Each external send is recorded locally (what, when, to
  which provider) so it is auditable after the fact.
- **No silent sends.** Ever.
- **No cloud-first default.** External use is always opt-in, never the path of
  least resistance.

## Relationship to configuration

`runa.yaml` already reserves a `privacy` block (see
[configuration.md](configuration.md)) with `mode`, `allow_external_providers`,
and `redact_before_provider`. Those fields are **documentation of intent** today:
v0.1 does not parse YAML and has no provider to gate. When parsing and providers
arrive, these modes are how that block should behave.

See also [safety-and-privacy.md](safety-and-privacy.md) and
[threat-model.md](threat-model.md).
