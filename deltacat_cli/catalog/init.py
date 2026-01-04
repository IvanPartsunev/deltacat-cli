from typing import Annotated

import typer
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from deltacat_cli.config import console
from deltacat_cli.utils.emojis import get_emoji
from deltacat_cli.utils.initialize_dc_catalog import initialize_catalog


app = typer.Typer()


def show_catalog_help() -> None:
    """Show catalog path options."""
    sections = [
        Text('🏠  Local filesystem:', style='bold green'),
        Text('  ~/.deltacat', style='dim'),
        Text(),
        Text('☁️  AWS S3:', style='bold blue'),
        Text('  s3://my-bucket/deltacat-root', style='dim'),
        Text(),
        Text('🌐  Google Cloud Storage:', style='bold yellow'),
        Text('  gs://my-bucket/deltacat-root', style='dim'),
        Text(),
        Text('🔷  Azure Blob Storage:', style='bold magenta'),
        Text('  abfs://container@account.dfs.core.windows.net/deltacat-root', style='dim'),
        Text(),
    ]

    # Use Group to properly stack the sections
    content = Group(*sections)

    console.print(
        Panel(content, title='[bold blue]Catalog Root Path Options[/bold blue]', border_style='green', padding=(1, 2))
    )


def show_help_callback(ctx: typer.Context, value: bool) -> bool:
    """Callback to handle --show-help flag before prompting."""
    if not value:
        return value
    if ctx.resilient_parsing:
        return value
    show_catalog_help()
    raise typer.Exit(0)


@app.command(name='init')
def initialize_cmd(
    show_help: Annotated[
        bool, typer.Option('--show-help', help='Show catalog path options and exit', callback=show_help_callback)
    ] = False,
    name: Annotated[str, typer.Option(help='Catalog name', prompt='Enter Catalog name')] = None,
    root: Annotated[str, typer.Option(help='Full catalog root path', prompt='Enter full Catalog root path')] = None,
) -> None:
    """Create and set a new Catalog."""

    try:
        console.print(
            f'{get_emoji("loading")} Initializing catalog "[cyan]{name}[/cyan]" at "[yellow]{root}[/yellow]"...'
        )
        initialize_catalog(catalog_name=name, root=root)
        console.print(f'{get_emoji("success")} Catalog initialized and set as current!', style='bold green')
    except Exception as e:
        console.print(f'{get_emoji("error")} Error initializing catalog: {e}', style='bold red')
        raise typer.Exit(1) from e
