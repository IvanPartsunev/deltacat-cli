import typer

from deltacat_cli.utils.catalog_context import catalog_context


app = typer.Typer()


@app.command(name='show')
def show_catalog_cmd() -> None:
    """Show the current active Catalog."""
    catalog_context.get_catalog_info(silent=False)

