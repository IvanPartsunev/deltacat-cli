from typing import Annotated

import typer
from deltacat import alter_namespace

from deltacat_cli.catalog.context import catalog_context
from deltacat_cli.config import console, err_console

app = typer.Typer()

@app.command()
def alter_namespace_cmd(
    name: Annotated[str, typer.Argument(help="Current namespace name")],
    new_name: Annotated[str, typer.Argument(help="New namespace name")]
):
    """
    Alter (rename) a namespace in the current catalog.
    
    Currently only supports renaming namespaces.
    """
    try:
        # Get current catalog info
        catalog_name, catalog_root = catalog_context.get_catalog_info()
        catalog = catalog_context.get_catalog()
        
        console.print(f'🔄 Renaming namespace "[bold cyan]{name}[/bold cyan]" to "[bold green]{new_name}[/bold green]" in catalog "[bold yellow]{catalog_name}[/bold yellow]"')
        
        alter_namespace(namespace=name, new_namespace=new_name, catalog=catalog)
        console.print(f'✅ Namespace renamed: [bold cyan]{name}[/bold cyan] → [bold green]{new_name}[/bold green]', style='green')
        
    except Exception as e:
        err_console.print(f'❌ Error altering namespace: {e}', style='bold red')
        raise typer.Exit(1) from e
