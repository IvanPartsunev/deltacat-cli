from typing import Annotated

import typer

from deltacat import read_table
from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji
from deltacat_cli.utils.error_handlers import handle_catalog_error


app = typer.Typer()


@app.command(name='read')
def read_table_cmd(
    name: Annotated[str, typer.Option(help='Table name to get')],
    namespace: Annotated[str, typer.Option(help='Namespace name where table is located')],
    columns: Annotated[str | None, typer.Option(help='Optional comma-separated column names to include.')] = None,
    table_version: Annotated[str | None, typer.Option(help='Optional specific version of the table to read')] = None,
    num_rows: Annotated[int, typer.Option(help='Number of rows to visualize. Default to 10.')] = 20,
) -> None:
    """
    Read the Table data with the given name and given namespace.
    If the table is empty TypeError will be raised `DataFrame.__init__() missing 1 required positional argument: 'builder'`
    """
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()
        console.print(f'{get_emoji("loading")} Read table "[cyan]{name}[/cyan]"')

        column_list = [key.strip() for key in columns.split(',') if key.strip()] if columns else None
        table = read_table(
            table=name, namespace=namespace, columns=column_list, table_version=table_version, catalog=catalog_name
        )
        console.print(f'{get_emoji("success")} Table "[bold cyan]{name}[/bold cyan]" read successfully', style='green')
        table.show(num_rows, format='markdown')

    except Exception as e:
        handle_catalog_error(e, 'read table')
