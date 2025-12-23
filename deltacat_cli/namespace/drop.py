from typing import Annotated

import typer

from deltacat import drop_namespace
from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji
from deltacat_cli.utils.error_handlers import handle_catalog_error


app = typer.Typer()


@app.command(name='drop')
def drop_namespace_cmd(
    name: Annotated[str, typer.Argument(help='Namespace name to drop')],
    purge: Annotated[bool, typer.Option(help='Purge all data (not implemented yet)')] = False,
    drop: Annotated[bool, typer.Option(prompt=True, confirmation_prompt=True)] = False,
) -> None:
    """Drop the Namespace with the given name."""
    if drop:
        try:
            catalog_name, _ = catalog_context.get_catalog_info(silent=True)
            catalog_context.get_catalog()
            console.print(
                f'{get_emoji("loading")} Dropping namespace "[cyan]{name}[/cyan]". Purge: "[green]{purge}[/green]"...'
            )

            drop_namespace(namespace=name, catalog=catalog_name)
            console.print(
                f'{get_emoji("success")} Namespace "[bold cyan]{name}[/bold cyan]" dropped successfully', style='green'
            )

        except Exception as e:
            handle_catalog_error(e, 'dropping namespace')
