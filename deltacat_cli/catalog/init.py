import typer
from google.api_core.path_template import expand
from rich.console import Group
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from deltacat_cli.config import console
from deltacat_cli.utils.initialize_dc_catalog import initialize_catalog


app = typer.Typer()


@app.command(name='init')
def initialize() -> None:
    sections = [
        Text("🏠 Local filesystem:", style="bold green"),
        Text("~/.deltacat", style="dim"),
        Text(),
        Text("☁️  AWS S3:", style="bold blue"),
        Text("s3://my-bucket/deltacat-root", style="dim"),
        Text(),
        Text("🌐 Google Cloud Storage:", style="bold yellow"),
        Text("gs://my-bucket/deltacat-root", style="dim"),
        Text(),
        Text("🔷 Azure Blob Storage:", style="bold magenta"),
        Text("abfs://container@account.dfs.core.windows.net/deltacat-root", style="dim")]

    # Use Group to properly stack the sections
    content = Group(*sections)

    console.print(Panel(
        content,
        title="[bold blue]Catalog Root Path Options[/bold blue]",
        border_style="green",
        padding=(1, 2),
        expand=False,
    ))
    root = Prompt.ask(
        '\n[bold green]Enter full Catalog root path[/bold green] [dim](see examples above)[/dim]',
        console=console,
    )

    catalog_name = Prompt.ask('\n[bold blue]Enter Catalog name[/bold blue]', console=console)

    try:
        console.print(f'🔄 Initializing catalog "[cyan]{catalog_name}[/cyan]" at "[yellow]{root}[/yellow]"...')
        initialize_catalog(catalog_name=catalog_name, root=root)
        console.print('🎉 Catalog initialized and set as current!', style='bold green')
    except Exception as e:
        console.print(f'❌ Error initializing catalog: {e}', style='bold red')
        raise typer.Exit(1) from e
