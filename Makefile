#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = AGENT INVESTIMENTO
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################



uv_install:
	uv pip install --upgrade pip && \
		uv pip install -r pyproject.toml

install:
	pip install --upgrade pip && \
		pip install -r pyproject.toml

import_format:
	uv run isort agente_investimento/ app/ 

format:
	uv run black agente_investimento/ app/ 

ruff_format:
	uv run ruff format agente_investimento/ app/ 

lint:
	uv run pylint --disable=R,C agente_investimento/ app/ 

ruff_lint:
	uv run ruff check agente_investimento/ app/ 

typepyright:
	uv run pyright agente_investimento/ app/ 

typemypy:
	uv run mypy agente_investimento/ app/ 

typepyrefly:
	uv run pyrefly check agente_investimento/ app/ 

## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	@echo ">>> Creating virtual environment using uv..."
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> Virtual environment created in .venv"
	@echo ">>> Activate it in your terminal with:"
	@echo ">>>   Windows: .\.venv\Scripts\activate"
	@echo ">>>   Unix/macOS: source ./.venv/bin/activate"

test:
	uv run -m pytest -vv --cov=tests/test_*.py

refactor: format lint

all: uv_install format lint typepyright  typepyrefly import_format ruff_format ruff_lint test