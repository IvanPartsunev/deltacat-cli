# DeltaCat CLI - Table Operations

The DeltaCat CLI provides comprehensive table management capabilities for working with DeltaCat tables. This module includes commands for creating, altering, retrieving, and dropping tables.

## Available Commands

- [`create`](#create) - Create a new DeltaCat table
- [`alter`](#alter) - Modify an existing table's properties and schema
- [`get`](#get) - Retrieve table information
- [`drop`](#drop) - Delete a table

## Command Reference

### create

Create a new DeltaCat table with specified schema and configuration.

```bash
deltacat table create --name TABLE_NAME --namespace NAMESPACE [OPTIONS]
```

#### Required Arguments

- `--name` - Unique identifier for your table
- `--namespace` - Logical grouping for tables (use default if unsure)

#### Optional Arguments

**Table Metadata:**
- `--table-description` - Description of the table for documentation purposes
- `--table-version` - Version identifier for the table
- `--table-version-description` - Description for the table version
- `--lifecycle-state` - Lifecycle state of the new table (default: ACTIVE)

**Schema Definition:**
- `--schema` - Column definitions in format "col1:type1,col2:type2"
- `--merge-keys` - Columns that uniquely identify records for updates (comma-separated)

**Table Properties:**
- `--read-optimization-level` - Read optimization level (NONE, MAX) - default: MAX
- `--default-compaction-hash-bucket-count` - Hash bucket count for compaction (default: 8)
- `--records-per-compacted-file` - Maximum records per compacted file (default: 4,000,000)
- `--appended-file-count-compaction-trigger` - Files that trigger compaction (default: 1000)
- `--appended-delta-count-compaction-trigger` - Deltas that trigger compaction (default: 100)
- `--schema-evolution-mode` - Schema evolution mode (AUTO, MANUAL, DISABLED) - default: AUTO
- `--default-schema-consistency-type` - Schema consistency type (NONE, VALIDATE, COERCE) - default: NONE

**Behavior Options:**
- `--fail-if-exists` - Raise error if table exists (default: True)
- `--auto-create-namespace` - Create namespace if it doesn't exist (default: True)

#### Data Types

The following data types are supported for schema definitions:

**Numeric Types:**
- `int64`, `int32` - Integer types
- `float64`, `float32` - Floating point types

**Text Types:**
- `string` - Text data

**Boolean Types:**
- `bool` - Boolean values

**Date/Time Types:**
- `date` - Date values
- `timestamp[s]`, `timestamp[ms]`, `timestamp[us]`, `timestamp[ns]` - Timestamp with different precisions
- `time[s]`, `time[ms]`, `time[us]`, `time[ns]` - Time values with different precisions

#### Examples

**Basic table creation:**
```bash
deltacat table create --name users --namespace prod
```

**Table with schema:**
```bash
deltacat table create \
  --name users \
  --namespace prod \
  --schema "id:int64,name:string,email:string,created_at:timestamp[s]" \
  --merge-keys "id"
```

**Event log table:**
```bash
deltacat table create \
  --name events \
  --namespace analytics \
  --schema "event_id:string,user_id:int64,timestamp:timestamp[s],data:string" \
  --merge-keys "event_id" \
  --table-description "User event tracking table"
```

**High-performance table with custom properties:**
```bash
deltacat table create \
  --name large_dataset \
  --namespace prod \
  --schema "id:int64,data:string,processed_at:timestamp[s]" \
  --merge-keys "id" \
  --records-per-compacted-file 8000000 \
  --default-compaction-hash-bucket-count 16 \
  --read-optimization-level MAX
```

### alter

Modify various aspects of an existing table's metadata, schema, and properties.

```bash
deltacat table alter --name TABLE_NAME --namespace NAMESPACE [OPTIONS]
```

#### Required Arguments

- `--name` - Name of the table to alter
- `--namespace` - Namespace of the table

#### Optional Arguments

**Table Metadata:**
- `--table-version` - Specific version to alter (defaults to latest active)
- `--lifecycle-state` - New lifecycle state (ACTIVE, DEPRECATED, etc.)
- `--table-description` - New description for the table
- `--table-version-description` - New description for the table version

**Schema Modifications:**
- `--schema-updates` - Add columns in format "new_col:type,another_col:type"
- `--remove-columns` - Remove columns (comma-separated column names)
- `--merge-keys` - Update merge key configuration

**Table Properties:**
- `--read-optimization-level` - Update read optimization level
- `--default-compaction-hash-bucket-count` - Update hash bucket count
- `--records-per-compacted-file` - Update records per file limit
- `--appended-file-count-compaction-trigger` - Update file count trigger
- `--appended-delta-count-compaction-trigger` - Update delta count trigger
- `--schema-evolution-mode` - Update schema evolution mode
- `--default-schema-consistency-type` - Update schema consistency type

#### Examples

**Update table description:**
```bash
deltacat table alter \
  --name users \
  --namespace prod \
  --table-description "Updated user data table with new fields"
```

**Change lifecycle state:**
```bash
deltacat table alter \
  --name old_events \
  --namespace analytics \
  --lifecycle-state DEPRECATED
```

**Add new columns:**
```bash
deltacat table alter \
  --name users \
  --namespace prod \
  --schema-updates "last_login:timestamp[s],status:string,score:float64"
```

**Remove columns:**
```bash
deltacat table alter \
  --name users \
  --namespace prod \
  --remove-columns "temp_field,old_column"
```

**Add and remove columns in one operation:**
```bash
deltacat table alter \
  --name users \
  --namespace prod \
  --schema-updates "new_field:int64,updated_field:string" \
  --remove-columns "deprecated_field,old_temp_column"
```

**Update merge keys:**
```bash
deltacat table alter \
  --name events \
  --namespace analytics \
  --merge-keys "user_id,event_timestamp"
```

**Update compaction settings:**
```bash
deltacat table alter \
  --name large_table \
  --namespace prod \
  --records-per-compacted-file 8000000 \
  --appended-file-count-compaction-trigger 500
```

### get

Retrieve detailed information about a table, including its schema, properties, and metadata.

```bash
deltacat table get --name TABLE_NAME --namespace NAMESPACE
```

#### Required Arguments

- `--name` - Name of the table to retrieve
- `--namespace` - Namespace where the table is located

#### Examples

**Get table information:**
```bash
deltacat table get --name users --namespace prod
```

The command returns detailed JSON information about the table including:
- Table metadata (name, description, lifecycle state)
- Schema definition with field types and merge keys
- Table properties and configuration
- Version information

### drop

Delete a table from the catalog. This operation requires confirmation.

```bash
deltacat table drop --name TABLE_NAME --namespace NAMESPACE [OPTIONS]
```

#### Required Arguments

- `--name` - Name of the table to drop
- `--namespace` - Namespace of the table

#### Optional Arguments

- `--purge` - Purge all data (not currently implemented)
- `--drop` - Confirmation flag (will prompt if not provided)

#### Examples

**Drop a table (with confirmation prompt):**
```bash
deltacat table drop --name old_table --namespace test
```

**Drop a table (skip confirmation prompt):**
```bash
deltacat table drop --name old_table --namespace test --drop
```

## Best Practices

### Schema Design

1. **Choose appropriate data types**: Use the most specific type that fits your data
2. **Define merge keys carefully**: These determine how records are updated during merges
3. **Plan for schema evolution**: Use AUTO schema evolution mode for flexibility

### Table Properties

1. **Optimize for your workload**:
   - Use `MAX` read optimization for read-heavy workloads
   - Use `NONE` for write-heavy workloads where compaction overhead is a concern

2. **Tune compaction settings**:
   - Increase `records-per-compacted-file` for larger datasets
   - Adjust `appended-file-count-compaction-trigger` based on write patterns
   - Use more hash buckets for better parallelism in large tables

3. **Schema consistency**:
   - Use `VALIDATE` for strict type checking
   - Use `COERCE` for automatic type conversion
   - Use `NONE` for maximum flexibility

### Naming Conventions

1. **Table names**: Use descriptive, lowercase names with underscores
2. **Namespaces**: Organize by environment (prod, staging, dev) or domain (analytics, user_data)
3. **Versions**: Use semantic versioning when specifying table versions

## Error Handling

The CLI provides detailed error messages for common issues:

- **TableAlreadyExistsError**: Table already exists (use `--fail-if-exists false` to ignore)
- **TableNotFoundError**: Table doesn't exist for alter/get/drop operations
- **SchemaValidationError**: Invalid schema definition or incompatible changes
- **TableValidationError**: Invalid table configuration or property values

## Integration with DeltaCat

These CLI commands directly interface with the DeltaCat catalog system:

- Tables are stored in the configured catalog backend
- Schema evolution follows DeltaCat's schema management rules
- Table properties control DeltaCat's optimization and compaction behavior
- All operations are transactional and maintain catalog consistency
