install:
	pip install uv && \
	uv pip install --upgrade pip && \
		uv pip install -r requirements.txt

format:
	black coleta_dados/*.py chat_bots/*.py

lint:
	pylint --disable=R,C coleta_dados/*.py chat_bots/*.py

typepyright:
	pyright coleta_dados/*.py chat_bots/*.py

typemypy:
	mypy coleta_dados/ chat_bots/

test:
	python -m pytest -vv --cov=tests/test_*.py

refactor: format lint

all: install lint format test typepyright