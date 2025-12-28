from typing import Annotated, List

import typer
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from deltacat import LifecycleState
from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji
from deltacat_cli.utils.error_handlers import handle_catalog_error
from deltacat_cli.utils.print_as_json import print_as_json
from deltacat_cli.utils.table_context import table_context


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
    name: Annotated[str, typer.Option(help='Table name to create', prompt=True)] = None,
    namespace: Annotated[str, typer.Option(help='Namespace name where table is located', prompt=True)] = None,
    table_description: Annotated[
        str, typer.Option(help='Description for the table', prompt=True, show_default=False)
    ] = '',
    table_version: Annotated[
        str, typer.Option(help='Table version of the table', prompt=True, show_default=False)
    ] = '',
    table_version_description: Annotated[
        str, typer.Option(help='Table version description', prompt=True, show_default=False)
    ] = '',
    schema: Annotated[
        str,
        typer.Option(
            help='Schema as key:type pairs (e.g., "id:int64,name:string")',
            prompt='Schema (key:type)',
            show_default=False,
        ),
    ] = '',
    merge_keys: Annotated[
        str,
        typer.Option(
            help='Column names to be used as merge keys (comma-separated)',
            prompt='Merge keys (comma-separated)',
            show_default=False,
        ),
    ] = '',
    lifecycle_state: Annotated[
        LifecycleState, typer.Option(help='Description for the table', prompt=True, case_sensitive=False)
    ] = LifecycleState.ACTIVE,
    compaction: Annotated[
        bool, typer.Option(help="If False table won't trigger automatic compaction", prompt=True)
    ] = True,
) -> None:
    """Create an empty Table with the given name, namespace."""
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()
        console.print(f'{get_emoji("loading")} Creating table "[cyan]{name}[/cyan]"')

        merge_keys_list = [key.strip() for key in merge_keys.split(',') if key.strip()] if merge_keys else None
        table_version = table_version if table_version else None

        schema_dict = (
            {pair.split(':', 1)[0].strip(): pair.split(':', 1)[1].strip() for pair in schema.split(',') if ':' in pair}
            if schema
            else None
        )

        table_description = table_description if table_description else None
        table_version_description = table_version_description if table_version_description else None

        # if not compaction:
        #     console.print('Compaction is disabled, merge_keys are set to `None`')

        table = table_context.create_table(
            name=name,
            namespace=namespace,
            catalog_name=catalog_name,
            table_version=table_version,
            merge_keys=merge_keys_list,
            lifecycle_state=lifecycle_state,
            schema=schema_dict,
            table_description=table_description,
            table_version_description=table_version_description,
            compaction=compaction,
        )
        print_as_json(source_type='table', data=table)

        console.print(
            f'{get_emoji("success")} Table "[bold cyan]{name}[/bold cyan]" created successfully', style='green'
        )

    except Exception as e:
        handle_catalog_error(e, 'creating table')
