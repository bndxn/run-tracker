.PHONY: install tests format


install:
	poetry install

tests:
	poetry run pytest


format: install
	poetry run isort .
