from typing import Annotated

import typer

from deltacat import alter_namespace
from deltacat_cli.config import console, err_console
from deltacat_cli.utils.catalog_context import catalog_context


app = typer.Typer()


@app.command(name='alter')
def alter_namespace_cmd(
    name: Annotated[str, typer.Argument(help='Current namespace name')],
    new_name: Annotated[str, typer.Argument(help='New namespace name')],
) -> None:
    """Alter (rename) a namespace in the current catalog.

    Currently only supports renaming namespaces.
    """
    try:
        # Get current catalog info
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        console.print(f'🔄 Renaming namespace "[cyan]{name}[/cyan]" to "[green]{new_name}[/green]"...')

        catalog_context.get_catalog()
        alter_namespace(namespace=name, new_namespace=new_name, catalog=catalog_name)

        console.print(f'✅ Namespace renamed: [bold cyan]{name}[/bold cyan] → [bold green]{new_name}[/bold green]', style='green')

    except Exception as e:
        err_console.print(f'❌ Error altering namespace: {e}', style='bold red')
        raise typer.Exit(1) from e
