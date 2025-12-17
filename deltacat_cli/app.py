"""Main CLI application for deltacat."""

import typer
from rich import print as rich_print

from deltacat_cli import __version__
from deltacat_cli.catalog import app as catalog_app
from deltacat_cli.config import SHOW_TRACEBACK, err_console
from deltacat_cli.namespace import app as namespace_app
from deltacat_cli.table import app as table_app


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        rich_print(f'deltacat version: {__version__}')
        raise typer.Exit(0)


app = typer.Typer(
    name='deltacat',
    help='A CLI application for working with deltacat',
    add_completion=False,
    pretty_exceptions_enable=not SHOW_TRACEBACK,
    pretty_exceptions_show_locals=SHOW_TRACEBACK,
)


@app.callback()
def main_callback(
    version: bool = typer.Option(
        False,
        '--version',
        '-v',
        callback=version_callback,
        is_eager=True,
        help='Show version and exit',
    ),
) -> None:
    """DeltaCat CLI - A command-line interface for working with deltacat.

    Use 'deltacat catalog init initialize' to get started.
    """


app.add_typer(catalog_app, name='catalog')
app.add_typer(namespace_app, name='namespace')
app.add_typer(table_app, name='table')


def main() -> None:
    """Entry point for the CLI application."""
    try:
        app()
    except Exception as e:
        if SHOW_TRACEBACK:
            raise
        err_console.print(f'❌ Error: {e}', style='bold red')
        raise typer.Exit(1) from e
