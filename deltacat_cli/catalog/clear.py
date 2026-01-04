import typer

from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji


app = typer.Typer()


@app.command(name='clear')
def clear_catalog_cmd() -> None:
    """Clear the current Catalog configuration."""
    success_msg = catalog_context.clear_catalog()
    console.print(f'{get_emoji("success")} {success_msg}', style='bold yellow')
