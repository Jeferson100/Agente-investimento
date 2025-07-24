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
	pip install uv && \
	uv pip install --upgrade pip && \
		uv pip install -r requirements.txt

install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

import_format:
	isort agente_investimento/ app/ tests/ 

format:
	black agente_investimento/ app/ tests/

ruff_format:
	ruff format agente_investimento/ app/ tests/

lint:
	pylint --disable=R,C agente_investimento/ app/ tests/

ruff_lint:
	ruff check agente_investimento/ app/ tests/

typepyright:
	pyright agente_investimento/ app/ tests/

typemypy:
	mypy agente_investimento/ app/ tests/

typepyrefly:
	pyrefly check agente_investimento/ app/ tests/

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
	python -m pytest -vv --cov=tests/test_*.py

refactor: format lint

all: install format lint typepyright typemypy import_format ruff_format ruff_lint test