# =============================================================================
# PDF Bulletin Processing — Developer Commands
# =============================================================================
# Usage:
#   make setup    — first-time setup (venv + dependencies + .env)
#   make install  — install / sync dependencies only
#   make start    — run the processing pipeline
#   make clean    — remove generated output files
#   make help     — show all available commands
# =============================================================================

PYTHON      := python3
VENV_DIR    := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python
ENV_FILE    := .env
ENV_EXAMPLE := .env.example

.DEFAULT_GOAL := help

# -----------------------------------------------------------------------------
# help — list all commands
# -----------------------------------------------------------------------------
.PHONY: help
help:
	@echo ""
	@echo "  PDF Bulletin Processing — available commands"
	@echo ""
	@echo "  make setup    First-time setup: create venv, install deps, copy .env"
	@echo "  make install  Install / sync dependencies into the venv"
	@echo "  make start    Run the processing pipeline"
	@echo "  make clean    Delete generated output files"
	@echo "  make help     Show this message"
	@echo ""

# -----------------------------------------------------------------------------
# setup — run this once after cloning the repo
# -----------------------------------------------------------------------------
.PHONY: setup
setup: $(VENV_DIR) install _copy_env
	@echo ""
	@echo "✅ Setup complete. Edit .env if needed, then run: make start"
	@echo ""

$(VENV_DIR):
	@echo "⏳ Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "   ✅ Virtual environment created at $(VENV_DIR)/"

_copy_env:
	@if [ ! -f $(ENV_FILE) ] && [ -f $(ENV_EXAMPLE) ]; then \
		cp $(ENV_EXAMPLE) $(ENV_FILE); \
		echo "   ✅ .env created from .env.example"; \
	elif [ ! -f $(ENV_FILE) ]; then \
		echo "   ⚠️  No .env found and no .env.example to copy from — skipping"; \
	else \
		echo "   ✅ .env already exists — skipping"; \
	fi

# -----------------------------------------------------------------------------
# install — sync dependencies (re-run after pulling changes)
# -----------------------------------------------------------------------------
.PHONY: install
install: $(VENV_DIR)
	@echo "⏳ Installing dependencies..."
	$(VENV_PYTHON) -m pip install --quiet --upgrade pip
	@if [ -f pyproject.toml ]; then \
		$(VENV_PYTHON) -m pip install --quiet -e .; \
	fi
	@echo "   ✅ Dependencies installed"

# -----------------------------------------------------------------------------
# start — run the pipeline
# -----------------------------------------------------------------------------
.PHONY: start
start:
	@echo "⏳ Starting pipeline..."
	$(VENV_PYTHON) main.py

# -----------------------------------------------------------------------------
# clean — remove generated files
# -----------------------------------------------------------------------------
.PHONY: clean
clean:
	@echo "🗑️  Removing generated output files..."
	@rm -f output/*.json
	@echo "   ✅ Done"
