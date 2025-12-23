from typing import Annotated

import typer

from deltacat import get_table
from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji
from deltacat_cli.utils.error_handlers import handle_catalog_error
from deltacat_cli.utils.print_as_json import print_as_json


app = typer.Typer()


@app.command(name='get')
def get_table_cmd(
    name: Annotated[str, typer.Argument(help='Table name to get')],
    namespace: Annotated[str, typer.Option(help='Namespace name where table is located')],
) -> None:
    """Get the Table definition with the given name and given namespace."""
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()
        console.print(f'{get_emoji("loading")} Get table "[cyan]{name}[/cyan]"')

        table = get_table(table=name, namespace=namespace, catalog=catalog_name)
        if not table:
            console.print(
                f'{get_emoji("empty")} No table with name {name} found in namespace: {namespace} in catalog: {catalog_name}',
                style='yellow',
            )
            raise typer.Exit(0)

        print_as_json(source_type='table', data=table)

        console.print(f'{get_emoji("success")} Table "[bold cyan]{name}[/bold cyan]" get successfully', style='green')

    except Exception as e:
        handle_catalog_error(e, 'get table')
