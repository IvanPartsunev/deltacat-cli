from typing import Annotated

import typer

from deltacat import get_namespace
from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import get_emoji
from deltacat_cli.utils.error_handlers import handle_catalog_error
from deltacat_cli.utils.print_as_json import print_as_json


app = typer.Typer()


@app.command(name='get')
def get_namespace_cmd(name: Annotated[str, typer.Option(help='Namespace name to get')]) -> None:
    """Get the Namespace with the given name."""
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()
        console.print(f'{get_emoji("loading")} Get namespace "[cyan]{name}[/cyan]"')

        namespace = get_namespace(namespace=name, catalog=catalog_name)
        if not namespace:
            console.print(f'{get_emoji("empty")} No namespace with name {name} found in this catalog', style='yellow')
            raise typer.Exit()

        print_as_json(source_type='namespace', data=namespace)

        console.print(
            f'{get_emoji("success")} Namespace "[bold cyan]{name}[/bold cyan]" get successfully', style='green'
        )

    except Exception as e:
        handle_catalog_error(e, 'get namespace')
