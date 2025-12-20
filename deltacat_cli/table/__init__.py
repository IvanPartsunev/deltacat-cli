"""Table operations for deltacat."""

import typer

from deltacat_cli.table.create import create_table
from deltacat_cli.table.info import show_info
from deltacat_cli.table.list import list_tables


app = typer.Typer(name='Table')

app.command(name='list', help=list_tables.__doc__)(list_tables)
app.command(name='create', help=create_table.__doc__)(create_table)
app.command(name='info', help=show_info.__doc__)(show_info)
