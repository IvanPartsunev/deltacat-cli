# DeltaCat CLI - Catalog Operations

The DeltaCat CLI catalog module provides commands for managing DeltaCat catalog configurations. A catalog defines where your DeltaCat data and metadata are stored.

## Available Commands

- [`init`](#init) - Initialize a new catalog
- [`set`](#set) - Set the current active catalog
- [`show`](#show) - Display current catalog information
- [`clear`](#clear) - Clear catalog configuration

## Command Reference

### init

Create and initialize a new DeltaCat catalog. This command sets up the catalog structure and makes it the active catalog for the current session.

```bash
deltacat catalog init [OPTIONS]
```

#### Options

- `--name` - Catalog name (will prompt if not provided)
- `--root` - Full catalog root path (will prompt if not provided)
- `--show-help` - Show catalog path options and examples

#### Supported Storage Backends

**Local Filesystem:**
```bash
deltacat catalog init --name local_catalog --root ~/.deltacat
```

**AWS S3:**
```bash
deltacat catalog init --name s3_catalog --root s3://my-bucket/deltacat-root
```

**Google Cloud Storage:**
```bash
deltacat catalog init --name gcs_catalog --root gs://my-bucket/deltacat-root
```

**Azure Blob Storage:**
```bash
deltacat catalog init --name azure_catalog --root abfs://container@account.dfs.core.windows.net/deltacat-root
```

#### Examples

**Interactive initialization:**
```bash
deltacat catalog init
# Will prompt for catalog name and root path
```

**Direct initialization:**
```bash
deltacat catalog init --name production --root s3://company-data/deltacat
```

**Show help with path examples:**
```bash
deltacat catalog init --show-help
```

### set

Set an existing catalog as the current active catalog for the session.

```bash
deltacat catalog set CATALOG_NAME --root ROOT_PATH
```

#### Arguments

- `CATALOG_NAME` - Name of the catalog to activate

#### Options

- `--root` - Root path of the catalog

#### Examples

**Set a local catalog:**
```bash
deltacat catalog set development --root ~/.deltacat/dev
```

**Set a cloud catalog:**
```bash
deltacat catalog set production --root s3://prod-bucket/deltacat
```

### show

Display information about the currently active catalog.

```bash
deltacat catalog show
```

This command shows:
- Current catalog name
- Catalog root path
- Connection status
- Configuration details

#### Examples

```bash
deltacat catalog show
# Output:
# ✅ Current Catalog: production
#    Root: s3://prod-bucket/deltacat
#    Status: Connected
```

### clear

Clear the current catalog configuration, removing the active catalog setting.

```bash
deltacat catalog clear
```

This command:
- Removes the current catalog configuration
- Requires you to set a new catalog before performing table operations
- Does not delete any data, only clears the local configuration

#### Examples

```bash
deltacat catalog clear
# Output:
# ⚠️  Catalog configuration cleared
```

## Catalog Configuration

### Storage Requirements

Different storage backends have different requirements:

**Local Filesystem:**
- Requires read/write permissions to the specified directory
- Automatically creates directory structure if it doesn't exist

**AWS S3:**
- Requires AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
- S3 bucket must exist and be accessible
- Requires `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`, and `s3:ListBucket` permissions

**Google Cloud Storage:**
- Requires Google Cloud credentials configured
- GCS bucket must exist and be accessible
- Requires appropriate IAM permissions for the bucket

**Azure Blob Storage:**
- Requires Azure credentials configured
- Storage account and container must exist
- Requires appropriate permissions for blob operations

### Best Practices

1. **Environment Separation**: Use different catalogs for different environments
   ```bash
   deltacat catalog init --name development --root ~/.deltacat/dev
   deltacat catalog init --name staging --root s3://staging-bucket/deltacat
   deltacat catalog init --name production --root s3://prod-bucket/deltacat
   ```

2. **Naming Conventions**: Use descriptive catalog names that indicate environment and purpose
   ```bash
   # Good examples
   deltacat catalog init --name prod_analytics --root s3://analytics-prod/deltacat
   deltacat catalog init --name dev_local --root ~/.deltacat/development
   
   # Avoid generic names
   deltacat catalog init --name catalog1 --root /tmp/deltacat
   ```

3. **Security**: 
   - Use appropriate access controls for cloud storage
   - Avoid storing sensitive catalogs in publicly accessible locations
   - Use IAM roles and policies to control access

4. **Backup**: Regularly backup your catalog metadata, especially for production environments

## Troubleshooting

### Common Issues

**Permission Errors:**
```bash
# Error: Access denied to s3://bucket/path
# Solution: Check AWS credentials and S3 permissions
aws sts get-caller-identity  # Verify AWS credentials
```

**Path Not Found:**
```bash
# Error: Cannot access catalog root path
# Solution: Verify the path exists and is accessible
# For S3: Check bucket exists and region is correct
# For local: Check directory permissions
```

**Catalog Already Exists:**
```bash
# Error: Catalog already initialized
# Solution: Use 'set' command instead of 'init', or choose a different name
deltacat catalog set existing_catalog --root /path/to/catalog
```

### Validation

After initializing a catalog, verify it's working:

```bash
# Check catalog status
deltacat catalog show

# Try creating a test namespace
deltacat namespace create --name test_namespace --description "Test namespace"

# List namespaces to verify catalog is working
deltacat namespace list
```

## Integration Notes

- Catalog configuration is stored locally and persists across CLI sessions
- Each catalog maintains its own namespace and table structure
- Switching catalogs changes the entire context for all subsequent operations
- Catalog operations are required before any table or namespace operations