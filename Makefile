install:
	pip install uv && \
	uv pip install --upgrade pip && \
		uv pip install -r requirements.txt

format:
	black coleta_dados/*.py chat_bots/*.py tratando_dados/*.py coleta_dados/fundamentos/*.py juncao_modelos_dados/*.py

ruff_format:
	ruff format chat_bots/*.py  coleta_dados/*.py tratando_dados/*.py coleta_dados/fundamentos/*.py juncao_modelos_dados/*.py

lint:
	pylint --disable=R,C coleta_dados/*.py chat_bots/*.py tratando_dados/*.py coleta_dados/fundamentos/*.py juncao_modelos_dados/*.py

ruff_lint:
	ruff check chat_bots/*.py  coleta_dados/*.py tratando_dados/*.py coleta_dados/fundamentos/*.py juncao_modelos_dados/*.py

typepyright:
	pyright coleta_dados/*.py chat_bots/*.py tratando_dados/*.py coleta_dados/fundamentos/*.py juncao_modelos_dados/*.py

typemypy:
	mypy coleta_dados/ chat_bots/ tratando_dados/ juncao_modelos_dados/

test:
	python -m pytest -vv --cov=tests/test_*.py

refactor: format lint

all: install format lint typepyright typemypy ruff_format ruff_lint