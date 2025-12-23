from typing import Annotated

import typer
from deltacat import LifecycleState

from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji
from deltacat_cli.utils.error_handlers import handle_catalog_error
from deltacat_cli.utils.print_as_json import print_as_json
from deltacat_cli.utils.table_context import table_context

app = typer.Typer()


@app.command(name='create')
def create_table_cmd(
    name: Annotated[str, typer.Option(help='Table name to create', prompt=True)],
    namespace: Annotated[str, typer.Option(help='Namespace name where table is located', prompt=True)],
    table_description: Annotated[
        str, typer.Option(help='Description for the table', prompt=True, show_default=False)
    ] = '',
    table_version: Annotated[str, typer.Option(help='Table version of the table', prompt=True, show_default=False)] = '',
    table_version_description: Annotated[str, typer.Option(help='Table version description', prompt=True, show_default=False)] = '',
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
    compaction: Annotated[bool, typer.Option(help='If False table won\'t trigger automatic compaction', prompt=True)] = True
) -> None:
    """Create an empty Table with the given name, namespace."""
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()
        console.print(f'{get_emoji("loading")} Creating table "[cyan]{name}[/cyan]"')

        merge_keys_list = [key.strip() for key in merge_keys.split(',') if key.strip()] if merge_keys and compaction else None
        table_version = table_version if table_version else None

        schema_dict = (
            {pair.split(':', 1)[0].strip(): pair.split(':', 1)[1].strip() for pair in schema.split(',') if ':' in pair}
            if schema
            else None
        )

        table_description = table_description if table_description else None
        table_version_description = table_version_description if table_version_description else None

        if not compaction:
            console.print('Compaction is disabled, merge_keys are set to `None`')

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
            compaction=compaction
        )
        print_as_json(source_type='table', data=table)

        console.print(
            f'{get_emoji("success")} Table "[bold cyan]{name}[/bold cyan]" created successfully', style='green'
        )

    except Exception as e:
        handle_catalog_error(e, 'creating table')
