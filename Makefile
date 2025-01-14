install:
	pip install uv && \
	uv pip install --upgrade pip && \
		uv pip install -r requirements.txt

format:
	black dados/*.py 

lint:
	pylint --disable=R,C dados/*.py 

typepyright:
	pyright dados/*.py 

typemypy:
	mypy dados/ 

test:
	python -m pytest -vv --cov=tests/test_*.py

refactor: format lint

all: install lint format test typepyright