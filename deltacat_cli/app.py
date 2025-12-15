"""Main CLI application for deltacat-cli."""

from typing import Annotated

import typer
from rich import print as rich_print

from deltacat_cli.config import app

from . import __version__


def name_callback(value: str) -> str:
    """Validate that only Camila is allowed as a name.

    Args:
        value: The name to validate.

    Returns:
        The validated name.

    Raises:
        typer.BadParameter: If the name is not Camila.
    """
    error_msg = 'Only Camila is allowed'
    if value != 'Camila':
        raise typer.BadParameter(error_msg)
    return value


@app.command()
def hello(
    name: Annotated[
        str | None,
        typer.Option(callback=name_callback, help='Name to greet (must be Camila)'),
    ] = None,
) -> None:
    """Greet someone with their name.

    Args:
        name: The name to greet (must be Camila).
    """
    rich_print(f'Hello {name}')


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
