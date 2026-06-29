# ADR 0002 — Operator, not agent

- **Status:** accepted
- **Date:** 2026-06-29

## Context

Runa is intended to help operate Markdown knowledge bases and project workflows.
It is local-first, Markdown-first, Git-first, proposal-first, append-first, and
explicit over magical.

The word "agent" can create the wrong expectation: autonomy, hidden decisions,
background execution, tool use without review, or AI-first behavior.

Runa's current behavior is intentionally much smaller and more inspectable:

- `scan` is read-only;
- `capture` is append-only;
- `propose` creates a separate proposal file;
- `ask` fails honestly in v0.1;
- there are no LLM calls, no RAG, no providers, and no autonomous behavior.

## Decision

Runa will describe itself primarily as an **operator** for Markdown knowledge
bases and project workflows, not as an autonomous agent.

The preferred short description is:

```text
Local-first, Markdown-first operator for knowledge bases and project workflows.
```

The project may still discuss agents when explaining what Runa is not, or when
describing future concepts, but "agent" should not be the primary positioning.

## Consequences

The project sets more accurate expectations.

Runa's identity stays aligned with proposal-first and human-reviewed workflows.

The project avoids AI hype and does not imply autonomy that does not exist.

## What this does not imply

This does not prevent future AI capabilities.

This does not prevent future local LLM integrations, provider abstractions,
personas, skills, or MCP support.

It only means those capabilities must remain explicit, bounded, inspectable, and
human-governed.
