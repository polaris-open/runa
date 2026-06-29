# Local Walkthrough

A guided 10–15 minute test of Runa v0.1 against the **synthetic** example vault.
Run everything from the repository root. Requires Python ≥ 3.11; no install, no
dependencies.

## What you will do

- run the local checks;
- inspect the synthetic vault;
- run `doctor` (read-only);
- run `scan` (read-only);
- copy the vault to `/tmp`;
- use `capture` (append-only);
- use `propose`;
- review the generated file under `proposals/` by hand;
- confirm existing notes were **not** changed;
- see that `ask` fails honestly.

## What this does not do

- does **not** use an LLM;
- does **not** use RAG;
- does **not** use embeddings;
- does **not** call the network;
- does **not** read any real/private vault;
- does **not** apply proposals automatically.

---

## Step 1 — Run checks

```bash
make check
```

You should see validation, the test suite, and a few CLI smoke checks pass.

## Step 2 — Inspect the example vault

```bash
find examples/vault-minimal -maxdepth 3 -type f | sort
```

Everything here is invented. There is no real data, no PII, no secrets.

## Step 3 — Run read-only commands

```bash
PYTHONPATH=src python -m runa doctor --vault examples/vault-minimal
PYTHONPATH=src python -m runa scan --vault examples/vault-minimal
```

`scan` only counts Markdown files and prints that nothing was sent anywhere.

## Step 4 — Work on a temporary copy

Never run write commands against a vault you care about. Use a throwaway copy:

```bash
rm -rf /tmp/runa-vault-test
cp -R examples/vault-minimal /tmp/runa-vault-test
```

## Step 5 — Capture an inbox entry

```bash
PYTHONPATH=src python -m runa capture --vault /tmp/runa-vault-test \
  --text "Synthetic walkthrough capture for Runa v0.1."
```

See the appended entry (capture only adds to the end):

```bash
tail -n 5 /tmp/runa-vault-test/inbox.md
```

## Step 6 — Create a proposal

```bash
PYTHONPATH=src python -m runa propose --vault /tmp/runa-vault-test \
  --title "Improve Polaris project note" \
  --body "Synthetic proposal created during the local walkthrough."
```

See the new proposal file (a separate file; your notes are untouched):

```bash
find /tmp/runa-vault-test/proposals -maxdepth 1 -type f | sort
```

Open it and read it — Runa proposes, it does not apply.

## Step 7 — Confirm source notes were not edited

```bash
diff -ru examples/vault-minimal/notes /tmp/runa-vault-test/notes || true
diff -ru examples/vault-minimal/projects /tmp/runa-vault-test/projects || true
```

There should be **no differences** in `notes/` or `projects/`. `propose` never
edits existing notes; `capture` only touched `inbox.md`.

## Step 8 — Try `ask`

```bash
PYTHONPATH=src python -m runa ask --vault examples/vault-minimal "What is this vault about?"
```

This should **fail honestly** with a message that `ask` is not implemented in
v0.1 (no retrieval, no LLM), and a non-zero exit code.

---

## Expected result

By the end you should see that:

- `scan` is read-only;
- `capture` is append-only;
- `propose` creates a separate file and leaves notes alone;
- `ask` does not exist yet;
- Runa v0.1 calls no network and no LLM;
- Runa is still a skeleton, not a finished product.

## Common mistakes

- running `capture` against a real vault (use the `/tmp` copy);
- expecting an AI answer (there is none yet);
- assuming a proposal is applied automatically (it is not);
- putting sensitive/real data in the `--text` or `--body` (keep it synthetic);
- mistaking this skeleton for a finished product.
