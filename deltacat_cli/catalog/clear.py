import typer

from deltacat_cli.catalog.context import catalog_context


app = typer.Typer()


@app.command()
def clear() -> None:
    """Clear the current catalog configuration."""
    catalog_context.clear_catalog()
