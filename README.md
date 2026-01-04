# DeltaCat CLI

A comprehensive command-line interface for working with DeltaCat, providing powerful tools for managing catalogs, namespaces, and tables in your data lake architecture.

## Features

- **Catalog Management**: Initialize, configure, and manage DeltaCat catalogs across multiple storage backends
- **Namespace Operations**: Create and organize logical data containers with rich metadata
- **Table Operations**: Full lifecycle management of DeltaCat tables with schema evolution
- **Multi-Backend Support**: Works with local filesystem, AWS S3, Google Cloud Storage, and Azure Blob Storage
- **Rich CLI Experience**: Interactive prompts, helpful error messages, and comprehensive help system
- **Shell Autocompletion**: Tab completion for all commands and options

## Installation

```bash
pip install deltacat-cli
```

## Quick Start

1. **Initialize a catalog:**
   ```bash
   deltacat catalog init --name my_catalog --root ~/.deltacat
   ```

2. **Create a namespace:**
   ```bash
   deltacat namespace create --name analytics --description "Analytics data"
   ```

3. **Create a table:**
   ```bash
   deltacat table create \
     --name user_events \
     --namespace analytics \
     --schema "user_id:int64,event_type:string,timestamp:timestamp[s]" \
     --merge-keys "user_id,timestamp"
   ```

4. **View your table:**
   ```bash
   deltacat table get --name user_events --namespace analytics
   ```

## Command Overview

### Catalog Operations
```bash
deltacat catalog init      # Initialize a new catalog
deltacat catalog set       # Set active catalog
deltacat catalog show      # Show current catalog info
deltacat catalog clear     # Clear catalog configuration
```

### Namespace Operations
```bash
deltacat namespace create  # Create a new namespace
deltacat namespace list    # List all namespaces
deltacat namespace get     # Get namespace details
deltacat namespace alter   # Modify namespace properties
deltacat namespace drop    # Delete a namespace
```

### Table Operations
```bash
deltacat table create     # Create a new table
deltacat table get        # Get table information
deltacat table alter      # Modify table schema and properties
deltacat table drop       # Delete a table
```

## Detailed Documentation

### 📁 [Catalog Operations](deltacat_cli/catalog/README.md)
Complete guide to catalog management including:
- Initializing catalogs on different storage backends (S3, GCS, Azure, local)
- Setting and switching between catalogs
- Configuration management and troubleshooting

### 🏷️ [Namespace Operations](deltacat_cli/namespace/README.md)
Comprehensive namespace management covering:
- Creating and organizing namespaces
- Best practices for namespace design patterns
- Properties and metadata management
- Environment and team-based organization strategies

### 📊 [Table Operations](deltacat_cli/table/README.md)
Full table lifecycle management including:
- Creating tables with rich schema definitions
- Schema evolution and table alteration
- Table properties and optimization settings
- Data types, merge keys, and compaction configuration

## Storage Backend Support

DeltaCat CLI supports multiple storage backends:

| Backend | URI Format | Example |
|---------|------------|---------|
| **Local Filesystem** | `file://` or absolute path | `~/.deltacat` or `/data/deltacat` |
| **AWS S3** | `s3://` | `s3://my-bucket/deltacat-root` |
| **Google Cloud Storage** | `gs://` | `gs://my-bucket/deltacat-root` |
| **Azure Blob Storage** | `abfs://` | `abfs://container@account.dfs.core.windows.net/deltacat-root` |

## Data Types

DeltaCat CLI supports a rich set of data types for table schemas:

| Category | Types | Example Usage |
|----------|-------|---------------|
| **Integers** | `int32`, `int64` | `user_id:int64` |
| **Floats** | `float32`, `float64` | `price:float64` |
| **Text** | `string` | `name:string` |
| **Boolean** | `bool` | `is_active:bool` |
| **Dates** | `date` | `birth_date:date` |
| **Timestamps** | `timestamp[s/ms/us/ns]` | `created_at:timestamp[s]` |
| **Time** | `time[s/ms/us/ns]` | `daily_time:time[s]` |

## Examples

### E-commerce Data Pipeline

```bash
# Initialize catalog
deltacat catalog init --name ecommerce --root s3://company-data/deltacat

# Create namespaces
deltacat namespace create --name production --description "Production e-commerce data"
deltacat namespace create --name analytics --description "Analytics and reporting data"

# Create user table
deltacat table create \
  --name users \
  --namespace production \
  --schema "user_id:int64,email:string,created_at:timestamp[s],is_active:bool" \
  --merge-keys "user_id" \
  --table-description "User account information"

# Create orders table
deltacat table create \
  --name orders \
  --namespace production \
  --schema "order_id:string,user_id:int64,amount:float64,order_date:timestamp[s],status:string" \
  --merge-keys "order_id" \
  --table-description "Customer orders"

# Create analytics table with custom properties
deltacat table create \
  --name user_metrics \
  --namespace analytics \
  --schema "user_id:int64,total_orders:int32,total_spent:float64,last_order_date:timestamp[s]" \
  --merge-keys "user_id" \
  --records-per-compacted-file 8000000 \
  --read-optimization-level MAX
```

### Schema Evolution Example

```bash
# Add new columns to existing table
deltacat table alter \
  --name users \
  --namespace production \
  --schema-updates "phone:string,country:string,subscription_tier:string"

# Update table properties
deltacat table alter \
  --name users \
  --namespace production \
  --table-description "Updated user table with contact info and subscription data" \
  --schema-evolution-mode AUTO
```

### Multi-Environment Setup

```bash
# Development environment
deltacat catalog init --name dev --root ~/.deltacat/dev
deltacat namespace create --name dev_analytics --properties environment=development

# Staging environment
deltacat catalog init --name staging --root s3://staging-bucket/deltacat
deltacat namespace create --name staging_analytics --properties environment=staging

# Production environment
deltacat catalog init --name prod --root s3://prod-bucket/deltacat
deltacat namespace create --name prod_analytics --properties environment=production

# Switch between environments
deltacat catalog set dev --root ~/.deltacat/dev
deltacat catalog set prod --root s3://prod-bucket/deltacat
```

## Shell Autocompletion

Enable tab completion for enhanced CLI experience:

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
- `deltacat table create --<TAB>` - shows available options
- `deltacat table create --schema "id:int64,name:<TAB>"` - shows data types

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DELTACAT_CLI_SHOW_TRACEBACK` | Show full error tracebacks | `false` |
| `DELTACAT_CLI_EMOJI_STYLE` | Emoji style (professional, colorful, minimal) | `professional` |

### Configuration Files

The CLI stores configuration in:
- **Catalog settings**: `~/.deltacat/cli/config.json`
- **Session data**: `~/.deltacat/cli/session.json`

## Troubleshooting

### Common Issues

**Catalog Connection Issues:**
```bash
# Check catalog status
deltacat catalog show

# Verify credentials for cloud storage
aws sts get-caller-identity  # For S3
gcloud auth list            # For GCS
az account show             # For Azure
```

**Permission Errors:**
```bash
# For S3 - check bucket permissions
aws s3 ls s3://your-bucket/

# For local filesystem - check directory permissions
ls -la ~/.deltacat/
```

**Schema Validation Errors:**
```bash
# Check supported data types
deltacat table create --show-types-help

# Validate schema format
deltacat table create --name test --namespace default --schema "id:int64,name:string"
```

### Getting Help

```bash
# General help
deltacat --help

# Command-specific help
deltacat table create --help
deltacat catalog init --show-help

# Show data types and examples
deltacat table create --show-types-help
```

## Development

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

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

### Code Quality

This project uses pre-commit hooks to maintain code quality. When you make changes:

```bash
# Run the same checks as CI
make pre-commit

# Or run individual tools if needed
uv run ruff check . --fix    # Fix linting issues
uv run ruff format .         # Fix formatting issues
```

**If CI fails due to formatting issues:**
1. Run `make pre-commit` locally (this runs the exact same checks as CI)
2. Commit and push the fixes
3. CI will pass on the next run

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
make test-unit           # Run unit tests
make build               # Build the package
make ci-local            # Run the same checks as CI locally
make release-check       # Full release validation
```

### Running Tests

```bash
# Run unit tests
make test-unit

# Run CLI tests
make test-cli

# Run all checks (same as CI)
make ci-local
```

### Testing

The project includes comprehensive unit tests for all CLI functionality:

- **Table Operations**: Tests for create, alter, get, and drop commands
- **Catalog Management**: Tests for catalog initialization and configuration
- **Namespace Operations**: Tests for namespace lifecycle management
- **Utility Functions**: Tests for schema parsing, table properties, and error handling
- **CLI Integration**: End-to-end tests for command-line interface

Run specific test categories:
```bash
# Test table operations
python -m pytest tests/test_table_cli.py -v

# Test with coverage
python -m pytest tests/ --cov=deltacat_cli --cov-report=html
```

## CI/CD

- **CI**: Runs linting, pre-commit hooks, CLI tests, and package building
- **Publishing**: Automatic PyPI publishing on GitHub releases

## License

Apache 2.0
