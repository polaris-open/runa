# Vault contract

A "vault" is just a directory of Markdown files. Runa keeps its expectations
minimal on purpose — it should work with vaults that already exist, including
Obsidian vaults, without reorganizing them.

## What Runa expects

- **Plain Markdown.** Content is `.md` files a human can read in any editor.
- **An optional `runa.yaml`.** If present, Runa knows the directory is a vault it
  may operate on. If absent, read-only commands still work.
- **An inbox file** (default `inbox.md`). Created on first `capture` if missing.
- **A `proposals/` directory.** Created on first `propose` if missing. Excluded
  from `scan`.
- **Note/project directories** such as `notes/` and `projects/`. Conventional,
  not required.

## What Runa ignores

When scanning, Runa skips these directories at any depth:

- `.git/`
- `.obsidian/`
- `proposals/`
- `__pycache__/`
- `.venv/`

This is what makes Runa **Obsidian-compatible but not Obsidian-dependent**: the
`.obsidian/` folder is ignored, and nothing about Obsidian is required.

## What Runa will not do

- It will not impose a rigid folder structure.
- It will not rewrite or reformat your existing notes.
- It will not move files around to fit a template.

## A minimal valid vault

```text
my-vault/
├── runa.yaml        # optional
├── inbox.md         # created by capture if missing
├── notes/           # optional
├── projects/        # optional
└── proposals/       # created by propose if missing
```

See [`examples/vault-minimal/`](../examples/vault-minimal/README.md) for a
working, synthetic example.
