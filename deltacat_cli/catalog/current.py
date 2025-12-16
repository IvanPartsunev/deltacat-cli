import typer

from deltacat_cli.catalog.context import catalog_context
from deltacat_cli.config import console


app = typer.Typer()

@app.command()
def show() -> None:
    """Show the current active catalog."""
    try:
        name, root = catalog_context.get_catalog_info()
        console.print(f'📌 Current catalog: [bold green]{name}[/bold green]')
        console.print(f'   Root: {root}', style='dim')
        console.print(f'   Full path: {root}/{name}', style='dim')
    except typer.Exit:
        pass  # Error already printed by get_catalog_info