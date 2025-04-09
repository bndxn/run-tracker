.PHONY: install tests format

install_poetry:
	pip install --upgrade pip
	pip install poetry

install:
	poetry install

tests:
	poetry run pytest

format:
	poetry run isort .
