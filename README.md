# Deltacat CLI

A command-line interface for working with deltacat.

[![CI](https://github.com/yourusername/deltacat-cli/workflows/CI/badge.svg)](https://github.com/yourusername/deltacat-cli/actions)

## Installation

```bash
pip install deltacat-cli
```

## Usage

```bash
# Show version
deltacat version

# Show help
deltacat --help

# Catalog operations
deltacat catalog init
deltacat catalog show
deltacat catalog set

# Namespace operations  
deltacat namespace --help
```

### Shell Autocompletion

To enable tab completion for the CLI commands:

```bash
# Automatic installation (recommended)
deltacat --install-completion

# Then restart your terminal - that's it!

# Alternative: Manual installation with instructions
deltacat completion --install

# Or show the completion script for manual setup
deltacat --show-completion
```

After installation, you can use tab completion:
- `deltacat <TAB>` - shows available commands
- `deltacat catalog <TAB>` - shows catalog subcommands
- `deltacat --<TAB>` - shows available options

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
make help                 # Show all available commands
make install             # Install package and dependencies
make install-completion  # Install shell autocompletion
make show-completion     # Show completion script
make format              # Format and fix code (linting + formatting)
make format-only         # Format code only (no linting fixes)
make lint                # Run linting checks
make check               # Run all checks
make test-cli            # Test CLI functionality
make build               # Build the package
make ci-local            # Run the same checks as CI locally
make release-check       # Full release validation
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
