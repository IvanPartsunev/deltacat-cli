# Makefile for deltacat-cli project
#
# IMPORTANT: 'make pre-commit' runs the EXACT same checks as CI
#
.PHONY: install help format lint test pre-commit clean build dev-setup

# === CORE COMMANDS ===

install: ## Install the package in development mode
	uv sync --dev
	@echo ""
	@echo "✅ Installation complete."
	@echo "💡 To enable shell autocompletion: deltacat --install-completion"

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

format: ## Format code only (no linting)
	@echo "🎨 Formatting code..."
	uv run --no-project ruff format .
	@echo "✅ Code formatting complete!"

lint: ## Run all linting checks and fixes
	@echo "🔍 Running linting checks with fixes..."
	uv run --no-project ruff check --fix .
	@echo "✅ Linting complete!"

lint-check: ## Check linting without making fixes
	@echo "🔍 Checking linting..."
	uv run --no-project ruff check .

test: ## Run all tests
	@echo "🧪 Running tests..."
	@echo "Testing CLI functionality:"
	uv run deltacat --version
	uv run deltacat --help >/dev/null
	@echo "✅ CLI tests passed!"
	@echo "💡 Add unit tests to tests/ directory for more comprehensive testing"

pre-commit: ## Run pre-commit hooks (same as CI)
	@echo "🔧 Running pre-commit hooks (same as CI)..."
	uv run pre-commit run --all-files
	@echo "🧪 Running basic CLI tests..."
	uv run deltacat --version
	uv run deltacat --help >/dev/null
	@echo "✅ CLI tests passed!"
	@echo "🚀 Pre-commit workflow complete!"
	@echo "✅ All checks passed - ready to commit!"

pre-commit-fix: ## Run pre-commit hooks with auto-fixes
	@echo "🔧 Running pre-commit hooks with auto-fixes..."
	@echo "🔍 Auto-fixing linting issues..."
	uv run --no-project ruff check --fix .
	@echo "🎨 Auto-formatting code..."
	uv run --no-project ruff format .
	@echo "🔧 Running remaining pre-commit hooks..."
	uv run pre-commit run --all-files
	@echo "🧪 Running basic CLI tests..."
	uv run deltacat --version
	uv run deltacat --help >/dev/null
	@echo "✅ CLI tests passed!"
	@echo "🚀 Pre-commit workflow complete!"
	@echo "✅ All checks passed - ready to commit!"

# === UTILITY COMMANDS ===

clean: ## Clean cache and temporary files
	@echo "🧹 Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache dist/ build/ 2>/dev/null || true
	@echo "✅ Cleanup complete!"

build: clean ## Build the package
	@echo "🏗️  Building package..."
	uv build
	@echo "✅ Package built successfully!"
	@ls -la dist/

dev-setup: install ## Complete development environment setup
	@echo "🚀 Development environment setup complete!"
	@echo "💡 Run 'make help' to see available commands"

# === CHECK COMMANDS ===

format-check: ## Check code formatting without making changes
	@echo "🔍 Checking code formatting..."
	uv run --no-project ruff format --check .

check: format-check lint-check ## Run all checks without making changes
	@echo "✅ All checks passed!"

# === CI/RELEASE COMMANDS ===

ci: check test build ## Run all CI checks (no fixes, just validation)
	@echo "✅ All CI checks passed!"

release-check: pre-commit build ## Full release validation (format, lint, test, build)
	@echo "🎯 Release check complete - package is ready!"

# === COMPLETION COMMANDS ===

install-completion: ## Install shell autocompletion
	@echo "🚀 Installing shell autocompletion..."
	uv run deltacat --install-completion
	@echo "✅ Autocompletion installed! Restart your terminal."

show-completion: ## Show completion script
	@echo "📋 Shell completion script:"
	uv run deltacat --show-completion

# === PUBLISH COMMANDS (use with caution) ===

publish-test: build ## Publish to TestPyPI
	@echo "🚀 Publishing to TestPyPI..."
	uv publish --repository testpypi dist/*

publish: build ## Publish to PyPI
	@echo "🚀 Publishing to PyPI..."
	@echo "⚠️  This will publish to production PyPI!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	uv publish dist/*
