"""Main CLI application for deltacat-cli."""

import typer

from deltacat_cli.version import app as version
from deltacat_cli.catalog import app as catalog_app
from deltacat_cli.table.app import app as table_app


app = typer.Typer(name='deltacat', help='A CLI application for working with deltacat', add_completion=False)

app.add_typer(version)
app.add_typer(catalog_app, name='catalog')
app.add_typer(table_app, name='table')

def main() -> None:
    """Entry point for the CLI application."""
    app()
