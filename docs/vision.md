# Vision

## The problem

Markdown vaults grow faster than people can maintain them. A vault that starts
as a few notes becomes hundreds of files: ideas, meeting notes, project logs,
half-finished thoughts. Over time it becomes hard to answer simple questions —
*what did I decide?*, *what is the status of this project?*, *where did that idea
go?* — without manually grepping through files.

The popular response is to point a chatbot at the folder. That can feel magical,
but it hides what changed and why, and it tends to treat your knowledge base as
disposable context for a model rather than as the durable thing it is.

## A different stance

> Runa is not a chatbot over notes.
> Runa is an operator for Markdown knowledge bases and project workflows.

An *operator* works **on** the vault with explicit, inspectable actions, the way
a careful collaborator would. It reads files, captures ideas, and **proposes**
changes — but it does not silently rewrite your knowledge.

> The default behavior should be local, explicit, inspectable, and reversible.

## Three things people confuse

- **Chatbot** — generates text in a conversation; the vault is just context.
- **Search** — finds files or passages; it does not act on them.
- **Vault operator** — reads, captures, and proposes structured changes to the
  vault itself, leaving a reviewable trail.

Runa aims to be the third. Search and (eventually) generation are tools it may
use, not the point.

## Why proposal-first

> If Runa wants to change knowledge, it should create a proposal before changing
> source files.

Proposals make change **reviewable** and **reversible**. You can read what Runa
suggests, keep it, edit it, or throw it away — and because vaults live in Git,
nothing is ever lost. This is the opposite of an assistant that edits your notes
in place and hopes you noticed.

The one allowed exception is `capture`: appending a timestamped idea to an inbox
is a direct, reversible action, so it does not need a proposal.

## Why local-first

Your knowledge is personal. The default must be that nothing leaves your machine
unless you explicitly choose otherwise. Runa is **cloud-capable, not
cloud-first**, and **LLM-neutral**: no provider is bundled, none is privileged,
and v0.1 makes no external calls at all.

## What success looks like

A tool that a careful person trusts enough to point at their real vault —
because it is local, explicit, and never changes their knowledge behind their
back.
