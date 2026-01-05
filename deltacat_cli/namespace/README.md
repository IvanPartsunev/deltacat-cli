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
deltacat namespace create --name NAMESPACE_NAME
```

#### Required Arguments

- `--name` - Unique name for the namespace

#### Examples

**Basic namespace creation:**
```bash
deltacat namespace create --name analytics
```

**Create namespace for different environments:**
```bash
deltacat namespace create --name production
deltacat namespace create --name staging
deltacat namespace create --name development
```

### alter

Rename an existing namespace in the current catalog.

```bash
deltacat namespace alter --name NAMESPACE_NAME --new-name NEW_NAME
```

#### Required Arguments

- `--name` - Current name of the namespace to alter
- `--new-name` - New name for the namespace

#### Examples

**Rename a namespace:**
```bash
deltacat namespace alter --name old_analytics --new-name analytics_v2
```

**Rename development namespace:**
```bash
deltacat namespace alter --name dev --new-name development
```

**Note:** Currently only supports renaming namespaces. Other alterations like description or properties are not yet implemented.

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

The command returns detailed JSON information about the namespace including metadata and configuration.

### list

List all namespaces in the current catalog.

```bash
deltacat namespace list
```

#### Examples

```bash
deltacat namespace list
```

This command displays all namespaces in the current catalog with their basic information.

### drop

Delete a namespace from the catalog.

```bash
deltacat namespace drop --name NAMESPACE_NAME [OPTIONS]
```

#### Required Arguments

- `--name` - Name of the namespace to drop

#### Optional Arguments

- `--purge` - Purge all data (not implemented yet) - default: no-purge
- `--drop` - Confirmation flag - default: no-drop

#### Examples

**Drop a namespace:**
```bash
deltacat namespace drop --name test_namespace --drop
```

**Note:** The `--purge` option is not yet implemented. Use `--drop` flag to confirm the operation.

## Namespace Design Patterns

### Environment-Based Organization

Organize namespaces by environment:

```bash
# Development environment
deltacat namespace create --name dev_analytics
deltacat namespace create --name dev_user_data

# Staging environment
deltacat namespace create --name staging_analytics
deltacat namespace create --name staging_user_data

# Production environment
deltacat namespace create --name prod_analytics
deltacat namespace create --name prod_user_data
```

### Domain-Based Organization

Organize namespaces by business domain:

```bash
# User domain
deltacat namespace create --name users

# Analytics domain
deltacat namespace create --name analytics

# Financial domain
deltacat namespace create --name finance

# ML domain
deltacat namespace create --name ml_features
```

### Team-Based Organization

Organize namespaces by team ownership:

```bash
# Data engineering team
deltacat namespace create --name data_eng

# Analytics team
deltacat namespace create --name analytics_team
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

Currently, the CLI supports basic namespace operations. Advanced features like custom properties and detailed metadata are not yet implemented but may be added in future versions.

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
   deltacat namespace drop --name unused_test_namespace --drop
   ```

2. **Migration planning**: Plan namespace changes carefully
   ```bash
   # Create new namespace
   deltacat namespace create --name new_analytics

   # Migrate tables (application-specific process)
   # ...

   # Drop old namespace after migration
   deltacat namespace drop --name old_analytics --drop
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
# Solution: Drop tables first or use --purge flag (when implemented)
# For now, manually drop all tables in the namespace first
deltacat table list --namespace data
# Drop each table individually, then drop the namespace
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
