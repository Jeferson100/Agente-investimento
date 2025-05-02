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
	isort coleta_dados/ chat_bots/ tratando_dados/ juncao_modelos_dados/ langgraph_construcao/ utils/ tests/

format:
	black coleta_dados/*.py chat_bots/*.py tratando_dados/*.py coleta_dados/fundamentos/*.py juncao_modelos_dados/*.py langgraph_construcao/*.py utils/*.py tests/*.py

ruff_format:
	ruff format chat_bots/*.py  coleta_dados/*.py tratando_dados/*.py coleta_dados/fundamentos/*.py juncao_modelos_dados/*.py langgraph_construcao/*.py utils/*.py tests/*.py

lint:
	pylint --disable=R,C coleta_dados/*.py chat_bots/*.py tratando_dados/*.py coleta_dados/fundamentos/*.py juncao_modelos_dados/*.py  langgraph_construcao/*.py utils/*.py tests/*.py

ruff_lint:
	ruff check chat_bots/*.py  coleta_dados/*.py tratando_dados/*.py coleta_dados/fundamentos/*.py juncao_modelos_dados/*.py langgraph_construcao/*.py utils/*.py tests/*.py

typepyright:
	pyright coleta_dados/*.py chat_bots/*.py tratando_dados/*.py coleta_dados/fundamentos/*.py juncao_modelos_dados/*.py langgraph_construcao/*.py utils/*.py tests/*.py

typemypy:
	mypy coleta_dados/ chat_bots/ tratando_dados/ juncao_modelos_dados/ langgraph_construcao/ utils/ tests/

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