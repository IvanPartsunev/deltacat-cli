"""Table operations for deltacat."""

import os

import typer

from deltacat_cli.config import console, err_console
from deltacat_cli.table.create import app as create_app
from deltacat_cli.table.create import create_table
from deltacat_cli.table.info import app as info_app
from deltacat_cli.table.info import show_info
from deltacat_cli.table.list import app as list_app
from deltacat_cli.table.list import list_tables


app = typer.Typer(name='Table')


@app.callback()
def table_callback() -> None:
    """Table operations for DeltaCat.

    All table commands require a catalog to be configured first.
    Use 'deltacat catalog init initialize' or 'deltacat catalog set' to configure a catalog.
    """
    # All table commands require a catalog to be set
    catalog_name = os.environ.get('DELTACAT_CLI_CATALOG_NAME')
    catalog_root = os.environ.get('DELTACAT_CLI_CATALOG_ROOT')

    if not catalog_name or not catalog_root:
        err_console.print('❌ No catalog configured in this session.', style='bold red')
        console.print(
            'Set catalog with: [bold cyan]deltacat catalog set[/bold cyan] or [bold cyan]deltacat catalog init initialize[/bold cyan]'
        )
        raise typer.Exit(1)


# Extract docstrings from the actual command functions
app.add_typer(list_app, name='list', help=list_tables.__doc__)
app.add_typer(create_app, name='create', help=create_table.__doc__)
app.add_typer(info_app, name='info', help=show_info.__doc__)
