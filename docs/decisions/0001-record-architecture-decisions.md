# ADR 0001 — Record architecture decisions

- **Status:** accepted
- **Date:** 2026-06-29

## Context

Runa is an early, local-first, Markdown-first project. Even at Draft v0.1, some
decisions are important enough to record explicitly because they affect project
identity, contributor expectations, and future technical direction.

Without lightweight decision records, the project may drift into accidental
architecture: features, technologies, or terms may be added because they are
popular rather than because they support Runa's principles.

## Decision

Runa will use lightweight Architecture Decision Records (ADRs) for decisions that
affect architecture, positioning, safety, privacy, runtime strategy, or major
product direction.

Each ADR should explain:

- context;
- decision;
- consequences;
- what the decision does not imply.

## Consequences

Important decisions become explicit and reviewable.

Future contributors can understand why the project made a decision before
reopening it.

The project avoids hiding architectural direction inside chat history, issues, or
unreviewed assumptions.

## What this does not imply

ADRs are not bureaucracy for every small change.

Small implementation details do not need ADRs.

ADRs can be superseded when the project learns, but changes should be deliberate.
