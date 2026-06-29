# ADR 0003 — Python for validation; Rust/Tauri as future evaluation candidates

- **Status:** accepted
- **Date:** 2026-06-29

## Context

Runa v0.1 is a runnable skeleton implemented in Python using only the standard
library at runtime. This keeps the project easy to inspect, easy to test, and
easy to change while the core domain is still being validated.

Runa's long-term direction may require a stronger local product foundation:

- fast filesystem operations;
- safe path handling;
- local indexing;
- Git integration;
- cross-platform binaries;
- desktop user experience;
- privacy-sensitive local workflows;
- eventual integration with local models and optional providers.

Rust could be a strong future fit for a product-grade local core.

Tauri could be a strong future fit for a lightweight cross-platform desktop
application, with a Rust backend and web-based UI.

However, adopting Rust or Tauri too early would increase complexity before the
project has validated its core behavior, contracts, proposal workflow, and local
search model.

## Decision

Python remains the implementation language for Runa v0.1 and v0.2.

Rust is a future candidate for a product-grade local core.

Tauri is a future candidate for a desktop application shell.

Runa will not migrate to Rust or introduce Tauri until the project has validated:

- local vault operations;
- proposal-first workflow;
- deterministic local search basics;
- safety and privacy boundaries;
- command semantics;
- contributor expectations.

Any future Rust/Tauri work should start as a spike or prototype, not a direct
rewrite.

## Consequences

Runa can keep iterating quickly in Python while the domain is still fluid.

The project avoids premature platform complexity.

The future direction is visible and intentional, so Python does not accidentally
become the final product architecture by inertia.

A future Rust/Tauri direction remains available without distracting v0.1/v0.2.

## What this does not imply

This does not mean Python is the final implementation language forever.

This does not mean Rust or Tauri are guaranteed.

This does not authorize a rewrite now.

This does not change the current no-LLM, no-RAG, no-provider scope of v0.1.
