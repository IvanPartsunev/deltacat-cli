from typing import Annotated

import typer

from deltacat import list_tables
from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji
from deltacat_cli.utils.error_handlers import handle_catalog_error
from deltacat_cli.utils.print_as_json import print_as_json


app = typer.Typer()


@app.command(name='list')
def list_tables_cmd(
    namespace: Annotated[str, typer.Option(help='Namespace from where to list tables.')],
    table: Annotated[
        str | None,
        typer.Option(
            help='Optional table to list its table versions. If not specified, lists the latest active version of each table in the namespace.'
        ),
    ] = None,
) -> None:
    """Get the Table definition with the given name and given namespace."""
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()
        console.print(f'{get_emoji("loading")} List tables in namespace: [cyan]{namespace}[/cyan]"')

        tables = list_tables(namespace=namespace, table=table, catalog=catalog_name)
        if not tables:
            console.print(
                f'{get_emoji("empty")} No tables found in namespace: {namespace} in catalog: {catalog_name}',
                style='yellow',
            )
            raise typer.Exit(0)

        for table in tables.all_items():
            print_as_json(source_type='table', data=table.table)

            console.print(
                f'{get_emoji("success")} Table "[bold cyan]{table.table.name}[/bold cyan]" get successfully',
                style='green',
            )

    except Exception as e:
        handle_catalog_error(e, 'get table')
