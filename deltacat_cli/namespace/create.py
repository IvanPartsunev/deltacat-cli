from typing import Annotated

import typer
from deltacat import create_namespace

from deltacat_cli.catalog.context import catalog_context
from deltacat_cli.config import console, err_console


app = typer.Typer()


@app.command()
def create_namespace_cmd(name: Annotated[str, typer.Argument(help='Namespace name to create')]) -> None:
    """Create a new namespace in the current catalog."""
    try:
        # Get current catalog info
        catalog_name, _ = catalog_context.get_catalog_info()
        catalog_context.get_catalog()

        console.print(
            f'🔄 Creating namespace "[bold cyan]{name}[/bold cyan]" in catalog "[bold yellow]{catalog_name}[/bold yellow]"'
        )

        create_namespace(namespace=name, catalog=catalog_name)
        console.print(f'✅ Namespace created: [bold cyan]{name}[/bold cyan]', style='green')

    except Exception as e:
        err_console.print(f'❌ Error creating namespace: {e}', style='bold red')
        raise typer.Exit(1) from e
