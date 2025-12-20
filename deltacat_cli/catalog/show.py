import typer

from deltacat_cli.utils.catalog_context import catalog_context


app = typer.Typer()


@app.command(name='show')
def show_catalog() -> None:
    """Show the current active catalog."""
    catalog_context.get_catalog_info()

