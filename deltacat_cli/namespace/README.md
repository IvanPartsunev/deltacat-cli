# DeltaCat CLI - Namespace Operations

The DeltaCat CLI namespace module provides commands for managing namespaces within a DeltaCat catalog. Namespaces are logical containers that organize tables and provide isolation between different datasets or environments.

## Available Commands

- [`create`](#create) - Create a new namespace
- [`alter`](#alter) - Modify an existing namespace
- [`get`](#get) - Retrieve namespace information
- [`list`](#list) - List all namespaces in the catalog
- [`drop`](#drop) - Delete a namespace

## Command Reference

### create

Create a new namespace in the current catalog.

```bash
deltacat namespace create --name NAMESPACE_NAME [OPTIONS]
```

#### Required Arguments

- `--name` - Unique name for the namespace

#### Optional Arguments

- `--description` - Description of the namespace
- `--properties` - Additional properties as key=value pairs (can be specified multiple times)

#### Examples

**Basic namespace creation:**
```bash
deltacat namespace create --name analytics
```

**Namespace with description:**
```bash
deltacat namespace create \
  --name user_data \
  --description "Contains all user-related tables and datasets"
```

**Namespace with properties:**
```bash
deltacat namespace create \
  --name production \
  --description "Production data namespace" \
  --properties owner=data-team \
  --properties environment=prod \
  --properties retention_days=365
```

### alter

Modify an existing namespace's properties or rename it.

```bash
deltacat namespace alter --name NAMESPACE_NAME [OPTIONS]
```

#### Required Arguments

- `--name` - Name of the namespace to alter

#### Optional Arguments

- `--new-name` - New name for the namespace (renames the namespace)
- `--description` - New description for the namespace
- `--properties` - Update properties as key=value pairs

#### Examples

**Update namespace description:**
```bash
deltacat namespace alter \
  --name analytics \
  --description "Updated analytics namespace with ML datasets"
```

**Rename a namespace:**
```bash
deltacat namespace alter \
  --name old_name \
  --new-name new_name
```

**Update namespace properties:**
```bash
deltacat namespace alter \
  --name production \
  --properties owner=new-team \
  --properties last_updated=2024-01-01
```

### get

Retrieve detailed information about a specific namespace.

```bash
deltacat namespace get --name NAMESPACE_NAME
```

#### Required Arguments

- `--name` - Name of the namespace to retrieve

#### Examples

```bash
deltacat namespace get --name analytics
```

The command returns detailed JSON information including:
- Namespace metadata (name, description, creation time)
- Properties and configuration
- Statistics (number of tables, etc.)

### list

List all namespaces in the current catalog.

```bash
deltacat namespace list [OPTIONS]
```

#### Optional Arguments

- `--format` - Output format (table, json) - default: table
- `--show-properties` - Include namespace properties in the output

#### Examples

**List namespaces in table format:**
```bash
deltacat namespace list
```

**List namespaces with properties:**
```bash
deltacat namespace list --show-properties
```

**List namespaces in JSON format:**
```bash
deltacat namespace list --format json
```

### drop

Delete a namespace from the catalog. This operation requires confirmation and will fail if the namespace contains tables.

```bash
deltacat namespace drop --name NAMESPACE_NAME [OPTIONS]
```

#### Required Arguments

- `--name` - Name of the namespace to drop

#### Optional Arguments

- `--force` - Force deletion even if namespace contains tables (use with caution)
- `--drop` - Confirmation flag (will prompt if not provided)

#### Examples

**Drop an empty namespace:**
```bash
deltacat namespace drop --name test_namespace
```

**Force drop a namespace with tables:**
```bash
deltacat namespace drop --name old_namespace --force --drop
```

## Namespace Design Patterns

### Environment-Based Organization

Organize namespaces by environment:

```bash
# Development environment
deltacat namespace create --name dev_analytics --description "Development analytics data"
deltacat namespace create --name dev_user_data --description "Development user data"

# Staging environment
deltacat namespace create --name staging_analytics --description "Staging analytics data"
deltacat namespace create --name staging_user_data --description "Staging user data"

# Production environment
deltacat namespace create --name prod_analytics --description "Production analytics data"
deltacat namespace create --name prod_user_data --description "Production user data"
```

### Domain-Based Organization

Organize namespaces by business domain:

```bash
# User domain
deltacat namespace create --name users --description "User profiles, authentication, preferences"

# Analytics domain
deltacat namespace create --name analytics --description "Event tracking, metrics, reporting"

# Financial domain
deltacat namespace create --name finance --description "Transactions, billing, revenue data"

# ML domain
deltacat namespace create --name ml_features --description "Machine learning features and models"
```

### Team-Based Organization

Organize namespaces by team ownership:

```bash
# Data engineering team
deltacat namespace create \
  --name data_eng \
  --description "Data engineering pipelines and infrastructure" \
  --properties team=data-engineering \
  --properties contact=data-eng@company.com

# Analytics team
deltacat namespace create \
  --name analytics_team \
  --description "Business analytics and reporting" \
  --properties team=analytics \
  --properties contact=analytics@company.com
```

## Best Practices

### Naming Conventions

1. **Use descriptive names**: Choose names that clearly indicate the namespace purpose
   ```bash
   # Good examples
   deltacat namespace create --name user_analytics
   deltacat namespace create --name financial_reporting
   deltacat namespace create --name ml_training_data

   # Avoid generic names
   deltacat namespace create --name data1
   deltacat namespace create --name temp
   ```

2. **Use consistent patterns**: Establish and follow naming conventions
   ```bash
   # Environment prefix pattern
   deltacat namespace create --name prod_user_data
   deltacat namespace create --name staging_user_data
   deltacat namespace create --name dev_user_data

   # Domain suffix pattern
   deltacat namespace create --name analytics_prod
   deltacat namespace create --name analytics_staging
   ```

3. **Use lowercase with underscores**: Follow standard naming conventions
   ```bash
   # Recommended
   deltacat namespace create --name user_behavior_analytics

   # Avoid
   deltacat namespace create --name UserBehaviorAnalytics
   deltacat namespace create --name user-behavior-analytics
   ```

### Properties and Metadata

1. **Document ownership**: Always specify who owns the namespace
   ```bash
   deltacat namespace create \
     --name critical_data \
     --properties owner=data-platform-team \
     --properties contact=data-platform@company.com
   ```

2. **Set retention policies**: Document data retention requirements
   ```bash
   deltacat namespace create \
     --name user_events \
     --properties retention_days=730 \
     --properties compliance=gdpr
   ```

3. **Environment tagging**: Tag namespaces with environment information
   ```bash
   deltacat namespace create \
     --name analytics \
     --properties environment=production \
     --properties criticality=high
   ```

### Security and Access Control

1. **Principle of least privilege**: Create namespaces with specific purposes
2. **Environment isolation**: Keep production and development data separate
3. **Sensitive data handling**: Use dedicated namespaces for PII or sensitive data

### Lifecycle Management

1. **Regular cleanup**: Remove unused namespaces
   ```bash
   # List all namespaces to identify unused ones
   deltacat namespace list

   # Drop unused namespaces
   deltacat namespace drop --name unused_test_namespace
   ```

2. **Migration planning**: Plan namespace changes carefully
   ```bash
   # Create new namespace
   deltacat namespace create --name new_analytics

   # Migrate tables (application-specific process)
   # ...

   # Drop old namespace after migration
   deltacat namespace drop --name old_analytics
   ```

## Error Handling

### Common Errors

**Namespace Already Exists:**
```bash
# Error: Namespace 'analytics' already exists
# Solution: Choose a different name or use alter command
deltacat namespace alter --name analytics --description "Updated description"
```

**Namespace Not Found:**
```bash
# Error: Namespace 'nonexistent' not found
# Solution: Check namespace name spelling or list available namespaces
deltacat namespace list
```

**Cannot Drop Non-Empty Namespace:**
```bash
# Error: Cannot drop namespace 'data' - contains tables
# Solution: Drop tables first or use --force flag
deltacat namespace drop --name data --force
```

**Permission Denied:**
```bash
# Error: Access denied when creating namespace
# Solution: Check catalog permissions and credentials
deltacat catalog show  # Verify catalog access
```

## Integration with Tables

Namespaces provide the organizational structure for tables:

```bash
# Create namespace
deltacat namespace create --name ecommerce

# Create tables within the namespace
deltacat table create --name users --namespace ecommerce
deltacat table create --name orders --namespace ecommerce
deltacat table create --name products --namespace ecommerce

# List tables in the namespace
deltacat table list --namespace ecommerce
```

## Default Namespace

DeltaCat provides a default namespace for tables created without specifying a namespace:

```bash
# This creates a table in the default namespace
deltacat table create --name test_table

# Equivalent to:
deltacat table create --name test_table --namespace default
```

The default namespace can be useful for:
- Quick testing and experimentation
- Simple single-namespace catalogs
- Temporary data that doesn't need organization
