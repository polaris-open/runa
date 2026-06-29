# Configuration — `runa.yaml`

A vault may contain a `runa.yaml` file describing how Runa should treat it. A
template lives at [`runa.yaml.example`](../runa.yaml.example).

> **Honest note:** Full YAML parsing is **not implemented** in the v0.1
> skeleton. v0.1 has no external dependencies (no PyYAML), so it only checks that
> a `runa.yaml` exists — `runa doctor` reports its presence. The fields below
> document **intent**; later versions will parse and honor them.

## Fields

```yaml
version: "0.1"

vault:
  root: "."                  # vault root, relative to the config file
  inbox: "inbox.md"          # capture target (append-only)
  proposals: "proposals"     # directory for generated proposals
  include:                   # which files count as content
    - "notes/**/*.md"
    - "projects/**/*.md"
    - "inbox.md"
  exclude:                   # what to skip
    - ".git/**"
    - ".obsidian/**"
    - "proposals/**"

privacy:
  mode: "local-first"        # default operating mode
  allow_external_providers: false
  redact_before_provider: true

behavior:
  default_write_mode: "proposal"   # changes are proposed, not applied
  capture_mode: "append"           # capture only appends

persona:
  default: "neutral"         # no hardcoded character

providers:
  default: "none"            # no provider bundled or enabled
```

## What v0.1 actually reads

- Whether `runa.yaml` exists (used by `doctor`).
- Its raw text, for display only — it is **not** interpreted.

The `include`/`exclude` globs are documentation today; in v0.1, `scan` uses a
fixed ignore list (`.git`, `.obsidian`, `proposals`, `__pycache__`, `.venv`)
rather than these globs. See [vault-contract.md](vault-contract.md).
