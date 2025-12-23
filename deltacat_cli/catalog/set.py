from typing import Annotated

import typer

from deltacat_cli.utils.catalog_context import catalog_context


app = typer.Typer()


@app.command(name='set')
def set_catalog_cmd(name: Annotated[str, typer.Argument()], root: Annotated[str, typer.Option()]) -> None:
    """Set the current Catalog for this session."""
    catalog_context.set_catalog(name, root)
