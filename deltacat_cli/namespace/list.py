import json

import typer
from deltacat import list_namespaces
from rich.json import JSON
from rich.panel import Panel
from rich.syntax import Syntax

from deltacat_cli.config import console
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.error_handlers import handle_catalog_error
from deltacat_cli.utils.print_json import print_json
from deltacat_cli.utils.emojis import get_emoji

app = typer.Typer()


@app.command(name='list')
def list_namespace_cmd() -> None:
    """List all namespaces in the current catalog."""
    try:
        catalog_name, _ = catalog_context.get_catalog_info(silent=True)
        catalog_context.get_catalog()
        console.print(f'{get_emoji("loading")} Listing Namespaces in Catalog "[cyan]{catalog_name}[/cyan]"...')

        all_namespaces = list_namespaces(catalog=catalog_name).all_items()

        if not all_namespaces:
            console.print(f'{get_emoji("empty")} No namespaces found in this catalog', style='yellow')
            return

        for namespace in all_namespaces:
          print_json(source_type='namespace', data=namespace)

        console.print(f'{get_emoji("success")} Found {len(all_namespaces)} namespace(s)', style='green')
        console.print()

    except Exception as e:
        handle_catalog_error(e, "listing namespaces")