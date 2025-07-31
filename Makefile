# Makefile for pycoreux development

.PHONY: help install install-dev test format lint clean build upload demo

help:
	@echo "Available commands:"
	@echo "  install     - Install package"
	@echo "  install-dev - Install package in development mode with dev dependencies"
	@echo "  test        - Run tests"
	@echo "  format      - Format code with black and isort"
	@echo "  lint        - Run mypy type checking"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build distribution packages"
	@echo "  upload      - Upload to PyPI (requires API token)"
	@echo "  demo        - Run demonstration script"
	@echo "  migrate     - Show migration guide"

install:
	pip install .

install-dev:
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -v

format:
	black .
	isort .

lint:
	mypy pycoreux/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload: build
	python -m twine upload dist/*

demo:
	python examples/demo.py

migrate:
	python migrate.py

# Development shortcuts
dev-setup: install-dev
	pre-commit install

test-all: format lint test

# Package verification
verify: build
	python -m twine check dist/*
