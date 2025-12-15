# Deltacat CLI

A command-line interface for working with deltacat.

[![CI](https://github.com/yourusername/deltacat-cli/workflows/CI/badge.svg)](https://github.com/yourusername/deltacat-cli/actions)

## Installation

```bash
pip install deltacat-cli
```

## Usage

```bash
# Greet someone (only Camila is allowed)
deltacat-cli hello --name Camila

# Show version
deltacat-cli version

# Show help
deltacat-cli --help
```

## Development

### Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/yourusername/deltacat-cli.git
cd deltacat-cli

# Install dependencies and setup development environment
make install
```

### Available Commands

```bash
make help              # Show all available commands
make format            # Format and fix code
make lint              # Run linting checks
make check             # Run all checks
make test-cli          # Test CLI functionality
make build             # Build the package
make ci-local          # Run the same checks as CI locally
make release-check     # Full release validation
```

### Running Tests

```bash
# Run CLI tests
make test-cli

# Run all checks (same as CI)
make ci-local

# Unit tests (commented out until real tests are added)
# make test-unit
```

## CI/CD

- **CI**: Runs linting, pre-commit hooks, CLI tests, and package building
- **Publishing**: Automatic PyPI publishing on GitHub releases

## License

Apache 2.0
