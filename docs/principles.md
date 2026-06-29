# Principles

These principles are the contract for how Runa should behave. When a design
decision is unclear, these win.

## Markdown-first

Plain `.md` files are the source of truth. Runa reads and writes Markdown that a
human can open in any editor. No proprietary format, no hidden database holding
the "real" version of your notes.

## Git-first

History, review, and recovery come from version control. Because the vault lives
in Git, every change Runa makes (or proposes) can be diffed, reviewed, and
reverted. Git is the safety net.

## Local-first

Everything runs on your machine by default. v0.1 makes **no network calls at
all**. Local is the default mode, not a fallback.

## Cloud-capable, not cloud-first

The architecture should allow optional cloud features later (sync, remote
providers), but the cloud must never be required to use Runa. If the network is
gone, Runa still works.

## Obsidian-compatible, not Obsidian-dependent

Runa works with Obsidian-style vaults (and ignores `.obsidian/`), but it does not
require Obsidian, its plugins, or its runtime. Your vault is just Markdown in a
folder.

## LLM-neutral / provider-neutral

No LLM provider is bundled, and none is privileged. The eventual provider
interface treats local runtimes and OpenAI-compatible APIs the same way. In v0.1
there is no provider at all.

## Proposal-first

> If Runa wants to change knowledge, it should create a proposal before changing
> source files.

Changes to knowledge are written as proposals for human review, not applied
silently. See [proposals.md](proposals.md).

## Append-first

`capture` only appends; it never rewrites a file. Capturing an idea is additive
and reversible. This is the single allowed exception to proposal-first, because
appending to an inbox is direct and safe.

## Safety-first

Refuse the obviously dangerous, stay inside the vault, and never destroy data.
Writes are scoped to the vault path; empty input is rejected; existing notes are
never overwritten by `propose`.

## Privacy-aware

Runa handles personal knowledge. Public examples must be synthetic, secrets must
never be committed, and nothing is sent to a provider without an explicit,
future, opt-in decision. See [safety-and-privacy.md](safety-and-privacy.md).

## Explicit over magical

Prefer behavior the user can see and predict over behavior that feels clever but
hides what happened. No surprise edits, no hidden network calls, no implicit
state.
