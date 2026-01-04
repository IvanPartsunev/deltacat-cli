import typer
from rich import print as rich_print

from deltacat_cli import __version__


app = typer.Typer()


@app.command()
def version() -> None:
    """Show the version of deltacat."""
    rich_print(f'deltacat version: {__version__}')
