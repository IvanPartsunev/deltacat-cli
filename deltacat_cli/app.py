"""Main CLI application for deltacat-cli."""

import typer
from rich import print as rich_print

from deltacat_cli import __version__
from deltacat_cli.catalog.app import app as catalog_app
from deltacat_cli.table.app import app as table_app


app = typer.Typer(
    name='deltacat-cli',
    help='A CLI application for working with deltacat',
    add_completion=False,
)

app.add_typer(catalog_app, name='catalog')
app.add_typer(table_app, name='table')


@app.command()
def version() -> None:
    """Show the version of deltacat-cli."""
    rich_print(f'deltacat-cli version: {__version__}')


def main() -> None:
    """Entry point for the CLI application."""
    app()


# Optional: allows running with `python -m deltacat_cli.app`
if __name__ == '__main__':
    main()
