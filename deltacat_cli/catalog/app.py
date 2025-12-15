"""Catalog management commands."""

import typer
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from deltacat_cli.catalog.context import catalog_context
from deltacat_cli.catalog.operations import initialize_catalog
from deltacat_cli.config import console


app = typer.Typer(name='Catalog')


@app.command()
def init() -> None:
    """Initialize a new DeltaCat catalog with interactive prompts."""
    # Display examples and explanation for catalog root
    examples_text = Text()
    examples_text.append('\nCatalog Root Path Options:\n\n', style='bold cyan')

    examples_text.append('🏠 Local filesystem:\n', style='bold green')
    examples_text.append('   ~/.deltacat\n\n', style='dim')

    examples_text.append('☁️  AWS S3:\n', style='bold blue')
    examples_text.append('   s3://my-bucket/deltacat-root\n\n', style='dim')

    examples_text.append('🌐 Google Cloud Storage:\n', style='bold yellow')
    examples_text.append('   gs://my-bucket/deltacat-root\n\n', style='dim')

    examples_text.append('🔷 Azure Blob Storage:\n', style='bold magenta')
    examples_text.append('   abfs://container@account.dfs.core.windows.net/deltacat-root\n\n', style='dim')

    examples_text.append("⚠️ If catalog doesn't exist, a new catalog will be created\n", style='bold red')

    console.print(Panel(examples_text, title='DeltaCat Catalog Configuration', border_style='blue'))

    # Get catalog root with enhanced prompt
    root = Prompt.ask(
        '\n[bold cyan]Enter full Catalog root path[/bold cyan] [dim](see examples above)[/dim]',
        console=console,
        default='deltacat',
    )

    # Get catalog name
    catalog_name = Prompt.ask('\n[bold cyan]Enter Catalog name[/bold cyan]', console=console, default='default')

    console.print(f"\n✅ Initializing catalog '[bold]{catalog_name}[/bold]' at '[bold]{root}[/bold]'", style='green')

    try:
        initialize_catalog(catalog_name=catalog_name, root=root)
        console.print('🎉 Catalog initialized and set as current!', style='bold green')
    except Exception as e:
        console.print(f'❌ Error initializing catalog: {e}', style='bold red')
        raise typer.Exit(1) from e


@app.command()
def set(catalog_name: str, root: str) -> None:
    """Set the current catalog for this session."""
    catalog_context.set_catalog(catalog_name, root)


@app.command()
def current() -> None:
    """Show the current active catalog."""
    try:
        name, root = catalog_context.get_catalog_info()
        console.print(f'📌 Current catalog: [bold green]{name}[/bold green]')
        console.print(f'   Root: {root}', style='dim')
        console.print(f'   Full path: {root}/{name}', style='dim')
    except typer.Exit:
        pass  # Error already printed by get_catalog_info


@app.command()
def clear() -> None:
    """Clear the current catalog configuration."""
    catalog_context.clear_catalog()
