from typing import Annotated

import typer

from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji


app = typer.Typer()


@app.command(name='set')
def set_catalog_cmd(name: Annotated[str, typer.Argument()], root: Annotated[str, typer.Option()]) -> None:
    """Set the current Catalog for this session."""
    success_msg, details = catalog_context.set_catalog(name, root)
    console.print(f'{get_emoji("success")} {success_msg}', style='green')
    for detail in details:
        console.print(detail, style='dim')
