import typer

from deltacat_cli.catalog.context import catalog_context


app = typer.Typer()

@app.command()
def set_catalog(catalog_name: str, root: str) -> None:
    """Set the current catalog for this session."""
    catalog_context.set_catalog(catalog_name, root)