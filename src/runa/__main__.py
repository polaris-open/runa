"""Module entry point so that ``python -m runa`` works.

Usage:
    PYTHONPATH=src python -m runa --help
"""

from runa.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
