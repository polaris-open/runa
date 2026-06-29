# Runa — developer tasks (standard library only, no install required).
PYTHON ?= python3
SRC := src
EXAMPLE_VAULT := examples/vault-minimal

.DEFAULT_GOAL := help

.PHONY: help validate test check demo clean

help: ## Show this help.
	@echo "Runa — available targets:"
	@echo "  make help      Show this help."
	@echo "  make validate  Run local repo hygiene checks (scripts/validate.py)."
	@echo "  make test      Run the unittest suite."
	@echo "  make check     Run validate + tests + basic CLI smoke checks."
	@echo "  make demo      Run --help, doctor and scan against the example vault."
	@echo "  make clean     Remove Python caches and build artifacts."

validate: ## Run local repo hygiene checks (no deps, no network).
	$(PYTHON) scripts/validate.py

test: ## Run the unittest suite.
	PYTHONPATH=$(SRC) $(PYTHON) -m unittest discover -s tests -v

check: validate test ## Run validate, tests, then basic CLI smoke checks.
	PYTHONPATH=$(SRC) $(PYTHON) -m runa --help
	PYTHONPATH=$(SRC) $(PYTHON) -m runa doctor --vault $(EXAMPLE_VAULT)
	PYTHONPATH=$(SRC) $(PYTHON) -m runa scan --vault $(EXAMPLE_VAULT)
	$(PYTHON) -m compileall $(SRC) tests

demo: ## Run --help, doctor and scan against the example vault.
	PYTHONPATH=$(SRC) $(PYTHON) -m runa --help
	PYTHONPATH=$(SRC) $(PYTHON) -m runa doctor --vault $(EXAMPLE_VAULT)
	PYTHONPATH=$(SRC) $(PYTHON) -m runa scan --vault $(EXAMPLE_VAULT)

clean: ## Remove Python caches and build artifacts.
	rm -rf build dist *.egg-info src/*.egg-info
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache
