from typing import Annotated

import typer

from deltacat import create_namespace
from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.error_handlers import handle_catalog_error


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
        handle_catalog_error(e, "creating namespace")
