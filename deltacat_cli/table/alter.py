from typing import Annotated

import typer
from deltacat.catalog.main.impl import get_table

import deltacat
from deltacat import LifecycleState, SchemaConsistencyType, SchemaEvolutionMode, TableReadOptimizationLevel, alter_table
from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji
from deltacat_cli.utils.error_handlers import handle_catalog_error
from deltacat_cli.utils.print_as_json import print_as_json
from deltacat_cli.utils.table_utils import DeltacatTableSchema, TableProperties, TableSchema


app = typer.Typer()


@app.command(name='alter')
def alter_table_cmd(
    name: Annotated[str, typer.Option(help='Name of the table to alter')],
    namespace: Annotated[str, typer.Option(help='Namespace of the table. Uses default namespace if not specified')],
    table_version: Annotated[
        str | None, typer.Option(help='Specific version of the table to alter. Defaults to the latest active version')
    ] = None,
    lifecycle_state: Annotated[
        LifecycleState | None, typer.Option(help='New lifecycle state for the table', case_sensitive=False)
    ] = None,
    schema_updates: Annotated[
        str | None,
        typer.Option(help='Schema updates to apply as key:type pairs (e.g., "new_col:string,updated_col:int64")'),
    ] = None,
    remove_columns: Annotated[
        str | None, typer.Option(help='Column names to be removed from table (comma-separated column names)')
    ] = None,
    merge_keys: Annotated[
        str | None, typer.Option(help='New merge keys for the table (comma-separated column names)')
    ] = None,
    table_description: Annotated[str | None, typer.Option(help='New description for the table')] = None,
    table_version_description: Annotated[
        str | None,
        typer.Option(help='New description for the table version. Defaults to table_description if not specified'),
    ] = None,
    read_optimization_level: Annotated[
        TableReadOptimizationLevel | None,
        typer.Option(
            help='New read optimization level (NONE, MAX). If set to NONE, table won\'t trigger automatic compaction, "MODERATE" is not implemented.',
            case_sensitive=False,
        ),
    ] = None,
    default_compaction_hash_bucket_count: Annotated[
        int | None, typer.Option(help='New default hash bucket count for compaction operations')
    ] = None,
    records_per_compacted_file: Annotated[
        int | None, typer.Option(help='New maximum number of records per compacted file')
    ] = None,
    appended_file_count_compaction_trigger: Annotated[
        int | None, typer.Option(help='New number of appended files that will trigger automatic compaction')
    ] = None,
    appended_delta_count_compaction_trigger: Annotated[
        int | None, typer.Option(help='New number of deltas that will trigger automatic compaction')
    ] = None,
    schema_evolution_mode: Annotated[
        SchemaEvolutionMode | None, typer.Option(help='New schema evolution mode', case_sensitive=False)
    ] = None,
    default_schema_consistency_type: Annotated[
        SchemaConsistencyType | None, typer.Option(help='New default schema consistency type', case_sensitive=False)
    ] = None,
) -> None:
    """
    Alter deltacat table/table_version definition.

    Modifies various aspects of a table's metadata, including lifecycle state, schema, description, and properties.

    REQUIRED ARGUMENTS:
    - name: Name of the table to alter
    - namespace: Namespace of the table

    OPTIONAL MODIFICATIONS:
    - lifecycle_state: Change table's lifecycle state
    - schema_updates: Add or remove columns in the table schema
    - merge_keys: Update the merge key configuration
    - table_description: Update table description
    - table_version_description: Update version-specific description
    - Various table properties for optimization and compaction

    EXAMPLES:
    # Update table description
    deltacat table alter --name users --namespace prod --table-description "Updated user data table"

    # Change lifecycle state
    deltacat table alter --name old_events --namespace analytics --lifecycle-state DEPRECATED

    # Add new columns to schema
    deltacat table alter --name users --namespace prod --schema-updates "last_login:timestamp[s],status:string"

    # Update merge keys
    deltacat table alter --name events --namespace analytics --merge-keys "user_id,event_timestamp"

    # Update compaction settings
    deltacat table alter --name large_table --namespace prod --records-per-compacted-file 8000000

    RAISES:
    - TableNotFoundError: If the table does not already exist
    - TableVersionNotFoundError: If the specified table version or active table version does not exist
    """
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()
        console.print(f'{get_emoji("loading")} Altering table "[cyan]{name}[/cyan]"...')

        table = get_table(table=name, namespace=namespace, table_version=table_version)

        dc_schema = None
        if schema_updates or remove_columns:
            # Get the original schema
            original_schema = table.table_version.schema
            schema_updates = TableSchema.of(schema_updates)

            # Apply updates
            dc_schema = DeltacatTableSchema.update(original_schema, schema_updates, remove_columns, merge_keys)

        # Prepare table properties if any property is specified
        table_properties = None
        if any(
            [
                read_optimization_level is not None,
                default_compaction_hash_bucket_count is not None,
                records_per_compacted_file is not None,
                appended_file_count_compaction_trigger is not None,
                appended_delta_count_compaction_trigger is not None,
                schema_evolution_mode is not None,
                default_schema_consistency_type is not None,
            ]
        ):
            table_properties = TableProperties.of(
                read_optimization_level,
                default_compaction_hash_bucket_count,
                records_per_compacted_file,
                appended_file_count_compaction_trigger,
                appended_delta_count_compaction_trigger,
                schema_evolution_mode,
                default_schema_consistency_type,
            )

        alter_table(
            table=name,
            namespace=namespace,
            catalog=catalog_name,
            table_version=table_version,
            lifecycle_state=lifecycle_state,
            schema_updates=dc_schema,
            table_description=table_description,
            table_version_description=table_version_description,
            table_properties=table_properties,
        )

        console.print(
            f'{get_emoji("success")} Table "[bold cyan]{name}[/bold cyan]" altered successfully.', style='green'
        )
        deltacat.refresh_table(table.table_version.name)
        print_as_json(source_type='table', data=table)

    except Exception as e:
        handle_catalog_error(e, 'altering table')
