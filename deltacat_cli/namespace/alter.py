from typing import Annotated

import typer

from deltacat import alter_namespace
from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.error_handlers import handle_catalog_error


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
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()  # Ensure catalog is registered with deltacat
        console.print(f'🔄 Renaming namespace "[cyan]{name}[/cyan]" to "[green]{new_name}[/green]"...')

        alter_namespace(namespace=name, new_namespace=new_name, catalog=catalog_name)

        console.print(
            f'✅ Namespace renamed: [bold cyan]{name}[/bold cyan] → [bold green]{new_name}[/bold green]', style='green'
        )

    except Exception as e:
        handle_catalog_error(e, 'altering namespace')
