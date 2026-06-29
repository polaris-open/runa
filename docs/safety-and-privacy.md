# Safety and privacy

Runa operates on personal knowledge, so safety and privacy are part of the
design, not an afterthought.

## Use a copy until you trust the tool

- **Do not point Runa at a real, sensitive vault before you understand it.** When
  experimenting, run against a copy.
- Read-only commands (`scan`, `doctor`) are safe by design, but build trust
  before using write commands on anything you care about.

## Nothing leaves your machine (in v0.1)

- v0.1 has **no provider and no network code**: it cannot send your data
  anywhere.
- When providers arrive (v0.3), the default will remain `local-first`, and
  sending anything to an external provider will require an explicit, configured,
  opt-in decision — ideally with redaction first. See
  [providers.md](providers.md).

## Proposal-first and append-first

- Runa does not edit source notes silently. Changes are written as proposals you
  review. See [proposals.md](proposals.md).
- `capture` is the only direct write, and it is append-only and reversible.
- Writes are scoped to the vault path; Runa refuses to write outside it.

## Never commit secrets or PII

- **Public examples must be synthetic.** Do not add real data, secrets, tokens,
  credentials, corporate information, or PII to the repository.
- The CLI prints a *hint* if captured/proposed text contains obvious patterns
  (for example, `password`, `token`, `secret`). This is a best-effort nudge, not
  a guarantee, and it never blocks you — treat it as a reminder, not a filter.
- If you accidentally commit a secret, rotate it and scrub history.

## What this is not

- Not a security boundary, sandbox, or compliance control.
- Not a PII/secret scanner you should rely on.

It is a careful default posture: local, explicit, reversible. See
[principles.md](principles.md) and [SECURITY.md](../SECURITY.md).

## Going deeper

- [privacy-modes.md](privacy-modes.md) — the intended privacy modes
  (`local-only`, `local-redacted`, `external-explicit`, `external-disabled`).
  Today the effective behavior is `local-only`; the rest is planned.
- [threat-model.md](threat-model.md) — an initial, honest threat model with the
  status of each control (implemented / partial / planned / out of scope).
