# Makefile for deltacat-cli project
.PHONY: install help format format-check lint lint-fix check pre-commit clean test-cli dev-setup

install: ## Install the package in development mode
	uv sync --dev
	uv run pre-commit install
	@echo ""
	@echo "Installation complete."
	@echo "Run the following command to activate the virtual environment:"
	@echo "  source .venv/bin/activate"
	@echo "Pre-commit hooks have been installed automatically."

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

format: ## Format code with ruff (includes import sorting and formatting)
	@echo "🔧 Running ruff linting with fixes..."
	uv run --no-project ruff check --fix .
	@echo "🎨 Running ruff formatting..."
	uv run --no-project ruff format .
	@echo "✅ Code formatting complete!"

format-check: ## Check code formatting without making changes
	@echo "🔍 Checking code formatting..."
	uv run --no-project ruff format --check .
	@echo "✅ Format check complete!"

lint: ## Lint code with ruff (check only, no fixes)
	@echo "🔍 Running ruff linting..."
	uv run --no-project ruff check .

lint-fix: ## Lint and auto-fix issues with ruff
	@echo "🔧 Running ruff linting with auto-fixes..."
	uv run --no-project ruff check --fix .
	@echo "✅ Linting fixes applied!"

check: ## Run all checks (lint + format check)
	@echo "🔍 Running comprehensive code checks..."
	@echo "Running linting..."
	uv run --no-project ruff check .
	@echo "Checking formatting..."
	uv run --no-project ruff format --check .
	@echo "✅ All checks passed!"

pre-commit: ## Run pre-commit hooks on all files
	@echo "🚀 Running pre-commit hooks on all files..."
	uv run pre-commit run --all-files

pre-commit-install: ## Install pre-commit hooks
	@echo "📦 Installing pre-commit hooks..."
	uv run pre-commit install
	@echo "✅ Pre-commit hooks installed!"

clean: ## Clean cache and temporary files
	@echo "🧹 Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache 2>/dev/null || true
	rm -rf .ruff_cache 2>/dev/null || true
	@echo "✅ Cleanup complete!"

test-cli: ## Test the CLI application with sample commands
	@echo "🧪 Testing CLI application..."
	@echo "Testing with valid name (Camila):"
	uv run python main.py --name Camila
	@echo ""
	@echo "Testing with invalid name (should fail):"
	uv run python main.py --name John || echo "✅ Validation working correctly!"
	@echo ""
	@echo "Testing help command:"
	uv run python main.py --help

test-cli-installed: ## Test the installed CLI command
	@echo "🧪 Testing installed CLI command..."
	@echo "Testing with valid name (Camila):"
	uv run deltacat-cli --name Camila
	@echo ""
	@echo "Testing with invalid name (should fail):"
	uv run deltacat-cli --name John || echo "✅ Validation working correctly!"

dev-setup: install ## Complete development environment setup
	@echo "🚀 Development environment setup complete!"
	@echo "Available commands:"
	@$(MAKE) help

# Convenience aliases for common workflows
fix: format ## Alias for format command (lint-fix + format)

all-checks: check pre-commit ## Run all possible checks (check + pre-commit)
	@echo "✅ All checks and hooks passed!"
