# Makefile for AI Prompt Lab

.PHONY: help install test lint format validate clean setup-hooks

help:
	@echo "AI Prompt Lab - Available Commands:"
	@echo ""
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code with black"
	@echo "  make validate     - Validate all prompts"
	@echo "  make clean        - Remove temporary files"
	@echo "  make setup-hooks  - Install git hooks"
	@echo "  make stats        - Show project statistics"
	@echo ""

install:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Dependencies installed"

test:
	. venv/bin/activate && pytest tests/ -v
	@echo "✅ Tests completed"

test-coverage:
	. venv/bin/activate && pytest tests/ --cov=core --cov-report=html --cov-report=term
	@echo "✅ Coverage report generated in htmlcov/"

lint:
	. venv/bin/activate && flake8 core/ tests/
	. venv/bin/activate && mypy core/
	@echo "✅ Linting completed"

format:
	. venv/bin/activate && black core/ tests/
	@echo "✅ Code formatted"

validate:
	. venv/bin/activate && python core/prompt_validator.py prompts/
	@echo "✅ Validation completed"

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned temporary files"

setup-hooks:
	chmod +x .githooks/pre-commit
	git config core.hooksPath .githooks
	@echo "✅ Git hooks installed"

stats:
	. venv/bin/activate && python core/cli.py stats

create:
	. venv/bin/activate && python core/cli.py create

list:
	. venv/bin/activate && python core/cli.py list
