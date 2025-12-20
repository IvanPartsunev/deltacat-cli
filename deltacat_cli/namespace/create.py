from typing import Annotated

import typer

from deltacat import create_namespace
from deltacat_cli.config import console, err_console
from deltacat_cli.utils.catalog_context import catalog_context


app = typer.Typer()


@app.command(name='create')
def create_namespace_cmd(name: Annotated[str, typer.Argument(help='Namespace name to create')]) -> None:
    """Create a new namespace in the current catalog."""
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        console.print(f'🔄 Creating namespace "[cyan]{name}[/cyan]" in catalog "[yellow]{catalog_name}[/yellow]"...')

        catalog_context.get_catalog()
        create_namespace(namespace=name, catalog=catalog_name)

        console.print(f'✅ Namespace "[bold cyan]{name}[/bold cyan]" created successfully', style='green')

    except Exception as e:
        err_console.print(f'❌ Error creating namespace: {e}', style='bold red')
        raise typer.Exit(1) from e
