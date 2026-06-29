# Security Policy

Runa is **Draft v0.1**. It runs locally, has no network calls, no authentication,
and no database. Even so, it operates on personal knowledge, so we take privacy
and safety seriously.

Organization-wide security defaults live in
[`polaris-open/.github`](https://github.com/polaris-open/.github). This file
covers Runa-specific notes.

## Reporting a vulnerability

- **Do not** open a public issue for a suspected vulnerability.
- Report it privately via the channels described in the organization policy in
  `polaris-open/.github` (for example, a private security advisory).
- Include steps to reproduce and the affected version/commit.

## Scope and expectations for v0.1

- Runa does not call external services or LLM providers in v0.1.
- Runa does not modify source notes silently; changes are proposed.
- `capture` is the only direct write and is append-only.

## Keeping the repository safe

- **Never commit secrets, tokens, credentials, or PII.** Public examples must be
  synthetic. See [docs/safety-and-privacy.md](docs/safety-and-privacy.md).
- Do not point Runa at a private or sensitive vault before you understand the
  tool. When experimenting, use a copy.
