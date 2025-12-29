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
from deltacat_cli.utils.table_utils import TableProperties, TableSchema


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
    show_help: Annotated[
        bool, typer.Option('--show-help', help='Show available data types and exit', callback=show_types_callback)
    ] = False,
    name: Annotated[str, typer.Option(help='Name of the table to create', prompt=True)] = None,
    namespace: Annotated[
        str, typer.Option(help='Optional namespace for the table. Uses default namespace if not specified', prompt=True)
    ] = None,
    table_description: Annotated[
        str, typer.Option(help='Optional description of the table', prompt=True, show_default=False)
    ] = '',
    table_version: Annotated[
        str, typer.Option(help='Optional version identifier for the table', prompt=True, show_default=False)
    ] = '',
    table_version_description: Annotated[
        str, typer.Option(help='Optional description for the table version', prompt=True, show_default=False)
    ] = '',
    schema: Annotated[
        str,
        typer.Option(
            help='Schema definition for the table as key:type pairs (e.g., "id:int64,name:string")',
            prompt='Schema (key:type)',
            show_default=False,
        ),
    ] = '',
    merge_keys: Annotated[
        str,
        typer.Option(
            help='Optional sort keys for the table (comma-separated)',
            prompt='Merge keys (comma-separated)',
            show_default=False,
        ),
    ] = '',
    lifecycle_state: Annotated[
        LifecycleState,
        typer.Option(help='Lifecycle state of the new table. Defaults to ACTIVE', prompt=True, case_sensitive=False),
    ] = LifecycleState.ACTIVE,
    fail_if_exists: Annotated[
        bool,
        typer.Option(
            help='If True, raises an error if table already exists. If False, returns existing table', prompt=True
        ),
    ] = True,
    auto_create_namespace: Annotated[
        bool, typer.Option(help="If True, creates the namespace if it doesn't exist. Defaults to False", prompt=True)
    ] = True,
    read_optimization_level: Annotated[
        TableReadOptimizationLevel,
        typer.Option(
            help="Read optimization level for the table. If set to `none` table won't trigger automatic compaction",
            prompt=True,
            case_sensitive=False,
        ),
    ] = TableReadOptimizationLevel.MAX,
    default_compaction_hash_bucket_count: Annotated[
        int, typer.Option(help='Default hash bucket count for compaction', prompt=True)
    ] = 8,
    records_per_compacted_file: Annotated[
        int, typer.Option(help='Maximum number of records per compacted file', prompt=True)
    ] = 4_000_000,
    appended_file_count_compaction_trigger: Annotated[
        int, typer.Option(help='Number of appended files that will trigger automatic compaction', prompt=True)
    ] = 1000,
    appended_delta_count_compaction_trigger: Annotated[
        int, typer.Option(help='Number of deltas that will trigger automatic compaction', prompt=True)
    ] = 100,
    schema_evolution_mode: Annotated[
        SchemaEvolutionMode, typer.Option(help='Schema evolution mode for the table', prompt=True, case_sensitive=False)
    ] = SchemaEvolutionMode.AUTO,
    default_schema_consistency_type: Annotated[
        SchemaConsistencyType,
        typer.Option(help='Default schema consistency type for the table', prompt=True, case_sensitive=False),
    ] = SchemaConsistencyType.NONE,
) -> None:
    """Create an empty Table with the given name, namespace, and properties"""
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()
        console.print(f'{get_emoji("loading")} Creating table "[cyan]{name}[/cyan]"')

        table_version = table_version if table_version else None

        table_description = table_description if table_description else None
        table_version_description = table_version_description if table_version_description else None

        schema = TableSchema.of(schema, merge_keys)
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
            schema=schema.deltacat_table_schema,
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
