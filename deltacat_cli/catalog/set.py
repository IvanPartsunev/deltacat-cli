import typer

from deltacat_cli.utils.catalog_context import catalog_context


app = typer.Typer()


@app.command(name='set')
def set_catalog_cmd(catalog_name: str, root: str) -> None:
    """Set the current Catalog for this session."""
    catalog_context.set_catalog(catalog_name, root)
