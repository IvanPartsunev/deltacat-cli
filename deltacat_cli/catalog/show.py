import typer

from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context


app = typer.Typer()


@app.command(name='show')
def show_catalog_cmd() -> None:
    """Show the current active Catalog."""
    title, details = catalog_context.get_catalog_display_info()
    console.print(title, style='green')
    for detail in details:
        console.print(detail, style='dim')
