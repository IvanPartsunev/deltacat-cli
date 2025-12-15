"""Main CLI application for deltacat-cli."""

from typing import Annotated

import typer
from rich import print as rich_print
from rich.console import Console
from rich.spinner import SPINNERS


# Register custom spinner
SPINNERS['cat'] = {
    'frames': ['😸', '😺', '😼'],
    'interval': 300,
}

app = typer.Typer()
console = Console()
err_console = Console(stderr=True)

existing_usernames = ['rick', 'morty']


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
def main(
    name: Annotated[str | None, typer.Option(callback=name_callback)] = None,
) -> None:
    """Main CLI command.

    Args:
        name: The name to greet (must be Camila).
    """
    rich_print(f'Hello {name}')


if __name__ == '__main__':
    app()
