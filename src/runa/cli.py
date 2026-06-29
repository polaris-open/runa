"""Runa command-line interface (argparse, standard library only).

Commands:
    doctor   Check that a vault looks usable.
    scan     Count Markdown files in a vault (read-only).
    capture  Append a timestamped note to the vault inbox (append-only).
    propose  Create a proposal file (never edits existing notes).
    ask      NOT implemented in v0.1 — fails honestly.

None of these commands access the network or call an LLM.
"""

from __future__ import annotations

import argparse
import sys

from runa import __version__, capture as capture_mod, config as config_mod
from runa import proposals as proposals_mod
from runa import safety, vault as vault_mod

_NO_EXTERNAL_NOTE = "No content was sent to any external provider. Runa v0.1 runs fully locally."


def _warn_if_sensitive(text: str) -> None:
    categories = safety.categorize_sensitive(text)
    if not categories:
        return
    summary = "; ".join(f"{cat}: {', '.join(labels)}" for cat, labels in categories.items())
    print(
        f"warning: input may contain sensitive data ({summary}).\n"
        "  In Runa v0.1 nothing leaves your machine; this text will still be written "
        "locally, exactly as you asked.\n"
        "  This is only a best-effort nudge, not a guarantee or a security boundary. "
        "Keep public examples synthetic.",
        file=sys.stderr,
    )


def cmd_doctor(args: argparse.Namespace) -> int:
    """Report whether a vault looks usable. No network, no LLM."""
    print(f"runa doctor — vault: {args.vault}")
    try:
        vault = vault_mod.resolve_vault(args.vault)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"  [FAIL] {exc}")
        return 1

    checks: list[tuple[bool, str]] = []
    checks.append((True, f"vault exists: {vault}"))

    config = config_mod.load_config(vault)
    checks.append((config["exists"], f"runa.yaml present: {config['exists']}"))

    inbox = vault / "inbox.md"
    checks.append((inbox.is_file(), f"inbox.md present: {inbox.is_file()}"))

    for name in ("notes", "projects", "proposals"):
        present = (vault / name).is_dir()
        checks.append((present, f"{name}/ present: {present}"))

    for ok, label in checks:
        marker = "ok " if ok else "warn"
        print(f"  [{marker}] {label}")

    # A vault is usable even without every optional directory; only a missing or
    # invalid vault path is a hard failure (already handled above).
    print(f"\n  {_NO_EXTERNAL_NOTE}")
    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    """Count Markdown files in a vault, read-only. No network, no LLM."""
    try:
        result = vault_mod.scan_vault(args.vault)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Vault: {result['vault']}")
    print(f"Markdown files: {result['markdown_files']}")
    top = result["top_level_directories"]
    print(f"Top-level directories: {', '.join(top) if top else '(none)'}")
    print(_NO_EXTERNAL_NOTE)
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    """Append a timestamped note to the inbox (append-only)."""
    try:
        safety.ensure_non_empty_text(args.text)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    _warn_if_sensitive(args.text)
    try:
        path = capture_mod.capture(args.vault, args.text)
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Captured (append-only) to: {path}")
    return 0


def cmd_propose(args: argparse.Namespace) -> int:
    """Create a proposal file without touching existing notes."""
    try:
        safety.ensure_non_empty_text(args.title)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    _warn_if_sensitive(f"{args.title}\n{args.body or ''}")
    try:
        path = proposals_mod.create_proposal(args.vault, args.title, args.body or "")
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Proposal created: {path}")
    print("No existing notes were modified. Review it manually; there is no apply step in v0.1.")
    return 0


def cmd_ask(args: argparse.Namespace) -> int:
    """Honest failure: retrieval and LLM calls do not exist in v0.1."""
    print(
        "`ask` is not implemented in v0.1. Runa does not perform retrieval or LLM calls yet.",
        file=sys.stderr,
    )
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="runa",
        description=(
            "Runa — Local-first, Markdown-first operator for knowledge bases and "
            "project workflows. Draft v0.1 (runnable skeleton): no LLM, no RAG, no "
            "external calls. Source files are never changed silently."
        ),
        epilog="Public examples use synthetic content only. See README.md and docs/.",
    )
    parser.add_argument("--version", action="version", version=f"runa {__version__}")

    sub = parser.add_subparsers(dest="command", metavar="<command>")

    doctor = sub.add_parser("doctor", help="Check that a vault looks usable.")
    doctor.add_argument("--vault", required=True, help="Path to the vault directory.")
    doctor.set_defaults(func=cmd_doctor)

    scan = sub.add_parser("scan", help="Count Markdown files in a vault (read-only).")
    scan.add_argument("--vault", required=True, help="Path to the vault directory.")
    scan.set_defaults(func=cmd_scan)

    capture = sub.add_parser(
        "capture", help="Append a timestamped note to the inbox (append-only)."
    )
    capture.add_argument("--vault", required=True, help="Path to the vault directory.")
    capture.add_argument("--text", required=True, help="Text to capture. Must not be empty.")
    capture.set_defaults(func=cmd_capture)

    propose = sub.add_parser(
        "propose", help="Create a proposal file (never edits existing notes)."
    )
    propose.add_argument("--vault", required=True, help="Path to the vault directory.")
    propose.add_argument("--title", required=True, help="Proposal title.")
    propose.add_argument("--body", default="", help="Proposal body / summary.")
    propose.set_defaults(func=cmd_propose)

    ask = sub.add_parser("ask", help="NOT implemented in v0.1 (fails honestly).")
    ask.add_argument("--vault", required=False, help="Path to the vault directory.")
    ask.add_argument("question", nargs="*", help="Question (ignored in v0.1).")
    ask.set_defaults(func=cmd_ask)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
