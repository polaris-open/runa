# Example vault — `vault-minimal`

This is a **fictional, synthetic** vault used to exercise the Runa CLI. It
contains no real data, no personal information, no secrets, and no company
information. Everything here is invented for demonstration.

Use it to try the read-only and append-only commands:

```bash
# from the repo root
PYTHONPATH=../../src python3 -m runa doctor --vault .
PYTHONPATH=../../src python3 -m runa scan --vault .
```

Or, from the repository root:

```bash
PYTHONPATH=src python3 -m runa doctor --vault examples/vault-minimal
PYTHONPATH=src python3 -m runa scan  --vault examples/vault-minimal
```

## Commands that write

`capture` and `propose` write into the vault. To avoid changing this versioned
example, run them against a temporary copy:

```bash
rm -rf /tmp/runa-vault-test
cp -R examples/vault-minimal /tmp/runa-vault-test

PYTHONPATH=src python3 -m runa capture --vault /tmp/runa-vault-test \
  --text "Synthetic test capture for Runa v0.1."

PYTHONPATH=src python3 -m runa propose --vault /tmp/runa-vault-test \
  --title "Improve project status note" \
  --body "Synthetic proposal created during validation."
```

## Layout

```text
vault-minimal/
├── runa.yaml            # vault configuration (not fully parsed in v0.1)
├── inbox.md             # capture target (append-only)
├── notes/               # free-form notes
│   └── ai-engineering.md
├── projects/            # project notes
│   └── polaris.md
└── proposals/           # where `runa propose` writes
    └── README.md
```
