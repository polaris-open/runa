# Proposals

Proposal-first is the core of how Runa changes knowledge.

> If Runa wants to change knowledge, it should create a proposal before changing
> source files.

## Why proposals exist

Editing someone's notes in place is fast but dangerous: it hides what changed and
why, and it erases the chance to say "no". Proposals invert that. Runa writes its
suggestion as a separate file you can read, diff, edit, keep, or delete. Because
the vault is in Git, nothing is lost either way.

This keeps Runa **explicit, inspectable, and reversible** — and clearly *not* a
chatbot quietly rewriting your knowledge base.

## How proposals are created (v0.1)

```bash
PYTHONPATH=src python -m runa propose --vault PATH \
  --title "Improve project status note" \
  --body "Short description of the suggested change."
```

This writes a file under `proposals/` named `<UTC-timestamp>-<slug>.md`
containing:

- the title,
- `Status: proposed`,
- the creation timestamp,
- a summary/body,
- a safety note,
- and explicitly **no** automatic apply.

Existing notes are never touched.

## What does NOT exist yet

- **No apply step.** v0.1 cannot turn a proposal into an edit of a source note.
- **No lifecycle beyond "proposed".** No accepted/rejected/applied states yet.
- **No Git automation.** You commit (or discard) changes yourself.

## Future apply flow (planned, not built)

Later versions (see [../ROADMAP.md](../ROADMAP.md), v0.4) intend to add:

- richer proposal states,
- a human-gated review/apply flow,
- Git integration so applying a proposal produces a reviewable commit.

Even then, applying will be a deliberate, human-confirmed action — never silent.
