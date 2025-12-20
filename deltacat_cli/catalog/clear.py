import typer

from deltacat_cli.utils.catalog_context import catalog_context


app = typer.Typer()


@app.command(name='clear')
def clear_catalog() -> None:
    """Clear the current catalog configuration"""
    catalog_context.clear_catalog()
