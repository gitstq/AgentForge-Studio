.PHONY: help install test lint clean fmt check

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	pip install -e ".[tui,dev]"

install-core: ## Install core package without optional dependencies
	pip install -e .

install-tui: ## Install with TUI support (rich)
	pip install -e ".[tui]"

test: ## Run tests with pytest
	python -m pytest tests/ -v

test-cov: ## Run tests with coverage report
	python -m pytest tests/ -v --cov=agentforge --cov-report=term-missing

lint: ## Run linting checks
	python -m py_compile agentforge/cli.py
	python -m py_compile agentforge/core/skill.py
	python -m py_compile agentforge/core/agent.py
	python -m py_compile agentforge/core/team.py
	python -m py_compile agentforge/core/engine.py
	python -m py_compile agentforge/templates/builtin.py
	python -m py_compile agentforge/export/mcp.py
	python -m py_compile agentforge/sandbox/tester.py
	python -m py_compile agentforge/tui/dashboard.py
	python -m py_compile agentforge/utils/file_io.py
	python -m py_compile agentforge/utils/validator.py

clean: ## Clean build artifacts and cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name *.egg-info -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/ 2>/dev/null || true

check: lint test ## Run lint and tests

init-demo: ## Initialize a demo project
	python -m agentforge.cli init

demo: ## Run a demo workflow
	python -m agentforge.cli template apply code-review my-reviewer
	python -m agentforge.cli skill list
	python -m agentforge.cli skill show my-reviewer
	python -m agentforge.cli skill test my-reviewer
	python -m agentforge.cli skill export my-reviewer --format mcp
