from typing import Annotated

import typer
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from deltacat import (
    LifecycleState,
    SchemaConsistencyType,
    SchemaEvolutionMode,
    TableReadOptimizationLevel,
    create_table,
)
from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji
from deltacat_cli.utils.error_handlers import handle_catalog_error
from deltacat_cli.utils.print_as_json import print_as_json
from deltacat_cli.utils.table_utils import DeltacatTableSchema, TableProperties, TableSchema


app = typer.Typer()


def show_type_help() -> None:
    """Show available data types in a panel."""
    type_sections = [Text('Available Data Types:', style='bold green'), Text()]

    # Group types by category
    numeric_types = ['int64', 'int32', 'float64', 'float32']
    text_types = ['string']
    boolean_types = ['bool']
    date_types = ['date', 'timestamp[s]', 'timestamp[ms]', 'timestamp[us]', 'timestamp[ns]']
    time_types = ['time[s]', 'time[ms]', 'time[us]', 'time[ns]']

    type_sections.append(Text('📊 Numeric Types:', style='bold blue'))
    for t in numeric_types:
        type_sections.append(Text(f'  {t}', style='dim'))
    type_sections.append(Text())

    type_sections.append(Text('📝 Text Types:', style='bold yellow'))
    for t in text_types:
        type_sections.append(Text(f'  {t}', style='dim'))
    type_sections.append(Text())

    type_sections.append(Text('✅ Boolean Types:', style='bold green'))
    for t in boolean_types:
        type_sections.append(Text(f'  {t}', style='dim'))
    type_sections.append(Text())

    type_sections.append(Text('📅 Date/Timestamp Types:', style='bold magenta'))
    for t in date_types:
        type_sections.append(Text(f'  {t}', style='dim'))
    type_sections.append(Text())

    type_sections.append(Text('⏰ Time Types:', style='bold cyan'))
    for t in time_types:
        type_sections.append(Text(f'  {t}', style='dim'))
    type_sections.append(Text())

    type_sections.append(Text('Example Schema:', style='bold white'))
    type_sections.append(Text('  "id:int64,name:string,created_at:timestamp[s]"', style='dim'))
    type_sections.append(Text())

    type_sections.append(Text('Example Merge Keys:', style='bold white'))
    type_sections.append(Text('  "id,timestamp" or "user_id"', style='dim'))

    content = Group(*type_sections)
    console.print(
        Panel(content, title='[bold blue]Table Creation Guide[/bold blue]', border_style='green', padding=(1, 2))
    )


def show_types_callback(ctx: typer.Context, value: bool) -> bool:
    """Callback to handle --show-types flag before prompting."""
    if not value:
        return value
    if ctx.resilient_parsing:
        return value
    show_type_help()
    raise typer.Exit(0)


@app.command(name='create')
def create_table_cmd(
    name: Annotated[str, typer.Option(help='Name of the table to create')],
    namespace: Annotated[
        str, typer.Option(help='Namespace for the table. If not specified, uses the default namespace')
    ],
    table_description: Annotated[
        str | None, typer.Option(help='Description of the table for documentation purposes', show_default=False)
    ] = None,
    table_version: Annotated[
        str | None, typer.Option(help='Version identifier for the table (optional)', show_default=False)
    ] = None,
    table_version_description: Annotated[
        str | None, typer.Option(help='Description for the table version (optional)', show_default=False)
    ] = None,
    schema: Annotated[
        str | None,
        typer.Option(
            help='Schema definition for the table as key:type pairs (e.g., "id:int64,name:string,created_at:timestamp[s]"). Use --show-help to see available data types',
            show_default=False,
        ),
    ] = None,
    merge_keys: Annotated[
        str | None,
        typer.Option(
            help='Merge keys for the table (comma-separated column names). These define how records are merged during updates',
            show_default=False,
        ),
    ] = None,
    lifecycle_state: Annotated[
        LifecycleState | None,
        typer.Option(help='Lifecycle state of the new table (ACTIVE, INACTIVE, DEPRECATED)', case_sensitive=False),
    ] = None,
    fail_if_exists: Annotated[
        bool, typer.Option(help='If True, raises an error if table already exists. If False, returns existing table')
    ] = True,
    auto_create_namespace: Annotated[
        bool, typer.Option(help="If True, creates the namespace if it doesn't exist")
    ] = True,
    read_optimization_level: Annotated[
        TableReadOptimizationLevel | None,
        typer.Option(
            help="Read optimization level (NONE, MIN, MAX). If set to NONE, table won't trigger automatic compaction",
            case_sensitive=False,
        ),
    ] = None,
    default_compaction_hash_bucket_count: Annotated[
        int | None, typer.Option(help='Default hash bucket count for compaction operations')
    ] = None,
    records_per_compacted_file: Annotated[
        int | None, typer.Option(help='Maximum number of records per compacted file')
    ] = None,
    appended_file_count_compaction_trigger: Annotated[
        int | None, typer.Option(help='Number of appended files that will trigger automatic compaction')
    ] = None,
    appended_delta_count_compaction_trigger: Annotated[
        int | None, typer.Option(help='Number of deltas that will trigger automatic compaction')
    ] = None,
    schema_evolution_mode: Annotated[
        SchemaEvolutionMode | None,
        typer.Option(help='Schema evolution mode (AUTO, STRICT, PERMISSIVE)', case_sensitive=False),
    ] = None,
    default_schema_consistency_type: Annotated[
        SchemaConsistencyType | None,
        typer.Option(help='Default schema consistency type (NONE, STRICT, EVENTUAL)', case_sensitive=False),
    ] = None,
    show_help: Annotated[
        bool,
        typer.Option(
            '--show-help',
            help='Show detailed help with available data types, examples, and best practices',
            callback=show_types_callback,
        ),
    ] = False,
) -> None:
    """
    Create a new DeltaCat table with specified schema and configuration.

    This command creates an empty table that can store structured data with versioning,
    schema evolution, and automatic compaction capabilities.

    REQUIRED ARGUMENTS:
    - name: Unique identifier for your table
    - namespace: Logical grouping for tables (use default if unsure)

    OPTIONAL ARGUMENTS:
    - schema: Column definitions in format "col1:type1,col2:type2" (can be added later)

    SCHEMA FORMAT:
    Define columns as comma-separated key:type pairs:
    - Basic: "id:int64,name:string"
    - With timestamps: "id:int64,name:string,created_at:timestamp[s]"
    - Mixed types: "user_id:int64,email:string,active:bool,score:float64"

    MERGE KEYS:
    Specify which columns uniquely identify records for updates:
    - Single key: "id"
    - Composite key: "user_id,timestamp"
    - No merge keys: "" (append-only table)

    EXAMPLES:
    # Create table without schema (schema can be defined later)
    deltacat table create --name users --namespace prod

    # Simple user table with schema
    deltacat table create --name users --namespace prod --schema "id:int64,name:string,email:string" --merge-keys "id"

    # Event log with timestamps
    deltacat table create --name events --namespace analytics --schema "event_id:string,user_id:int64,timestamp:timestamp[s],data:string" --merge-keys "event_id"

    # Financial data with composite keys
    deltacat table create --name trades --namespace finance --schema "symbol:string,timestamp:timestamp[ms],price:float64,volume:int64" --merge-keys "symbol,timestamp"

    Use --show-help to see all available data types and advanced configuration options.
    """
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()
        console.print(f'{get_emoji("loading")} Creating table "[cyan]{name}[/cyan]"')

        # Use defaults for None values
        lifecycle_state = lifecycle_state or LifecycleState.ACTIVE
        read_optimization_level = read_optimization_level or TableReadOptimizationLevel.MAX
        default_compaction_hash_bucket_count = default_compaction_hash_bucket_count or 8
        records_per_compacted_file = records_per_compacted_file or 4_000_000
        appended_file_count_compaction_trigger = appended_file_count_compaction_trigger or 1000
        appended_delta_count_compaction_trigger = appended_delta_count_compaction_trigger or 100
        schema_evolution_mode = schema_evolution_mode or SchemaEvolutionMode.AUTO
        default_schema_consistency_type = default_schema_consistency_type or SchemaConsistencyType.NONE

        table_schema = TableSchema.of(schema) if schema else None
        dc_schema = DeltacatTableSchema.of(table_schema, merge_keys) if table_schema else None

        table_properties = TableProperties.of(
            read_optimization_level,
            default_compaction_hash_bucket_count,
            records_per_compacted_file,
            appended_file_count_compaction_trigger,
            appended_delta_count_compaction_trigger,
            schema_evolution_mode,
            default_schema_consistency_type,
        )

        table = create_table(
            table=name,
            namespace=namespace,
            catalog=catalog_name,
            table_version=table_version,
            schema=dc_schema,
            table_description=table_description,
            table_version_description=table_version_description,
            lifecycle_state=lifecycle_state,
            fail_if_exists=fail_if_exists,
            auto_create_namespace=auto_create_namespace,
            table_properties=table_properties,
        )
        print_as_json(source_type='table', data=table)

        console.print(
            f'{get_emoji("success")} Table "[bold cyan]{name}[/bold cyan]" created successfully', style='green'
        )

    except Exception as e:
        handle_catalog_error(e, 'creating table')
