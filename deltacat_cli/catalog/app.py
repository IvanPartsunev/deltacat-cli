import typer
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from deltacat_cli.catalog.operations import initialize_catalog
from deltacat_cli.catalog.state import catalog_state
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
    examples_text.append(
        '   abfs://container@account.dfs.core.windows.net/deltacat-root\n\n',
        style='dim',
    )

    examples_text.append(
        "⚠️ If catalog don't exists new catalog will be created\n", style='bold red'
    )

    console.print(
        Panel(
            examples_text, title='DeltaCat Catalog Configuration', border_style='blue'
        )
    )

    # Get catalog root with enhanced prompt
    root = Prompt.ask(
        '\n[bold cyan]Enter full Catalog root path[/bold cyan] [dim](see examples above)[/dim]',
        console=console,
        default='deltacat',
    )

    # Get catalog name
    catalog_name = Prompt.ask(
        '\n[bold cyan]Enter Catalog name[/bold cyan]',
        console=console,
        default='default',
    )

    console.print(
        f"\n✅ Initializing catalog '[bold]{catalog_name}[/bold]' at '[bold]{root}[/bold]'",
        style='green',
    )

    try:
        initialize_catalog(catalog_name=catalog_name, root=root)
        console.print('🎉 Catalog initialized successfully!', style='bold green')
        console.print(f'📌 Catalog "{catalog_name}" is now active', style='cyan')
    except Exception as e:
        console.print(f'❌ Error initializing catalog: {e}', style='bold red')
        raise typer.Exit(1) from e


@app.command('list')
def list_catalogs() -> None:
    """List all configured catalogs."""
    catalogs = catalog_state.list_catalogs()
    current = catalog_state.get_current_catalog()

    if not catalogs:
        console.print('No catalogs configured.', style='yellow')
        console.print(
            'Initialize one with: [bold cyan]deltacat-cli catalog init[/bold cyan]'
        )
        return

    console.print('\n📚 Configured Catalogs:\n', style='bold cyan')

    for name, config in catalogs.items():
        is_current = current and current['name'] == name
        marker = '👉 ' if is_current else '   '
        style = 'bold green' if is_current else 'white'

        console.print(f'{marker}[{style}]{name}[/{style}]', style=style)
        console.print(f'    Root: {config["root"]}', style='dim')
        if is_current:
            console.print('    (current)', style='dim green')
        console.print()


@app.command()
def switch(catalog_name: str) -> None:
    """Switch to a different catalog."""
    try:
        catalog_state.set_current_catalog(catalog_name)
        console.print(f'🔄 Switched to catalog "{catalog_name}"', style='green')
    except Exception as e:
        console.print(f'❌ Error switching catalog: {e}', style='bold red')
        raise typer.Exit(1) from e


@app.command()
def current() -> None:
    """Show the current active catalog."""
    current = catalog_state.get_current_catalog()

    if not current:
        console.print('❌ No catalog is currently active.', style='bold red')
        console.print(
            'Initialize one with: [bold cyan]deltacat-cli catalog init[/bold cyan]'
        )
        return

    console.print(f'📌 Current catalog: [bold green]{current["name"]}[/bold green]')
    console.print(f'   Root: {current["root"]}', style='dim')


@app.command()
def remove(catalog_name: str) -> None:
    """Remove a catalog configuration."""
    try:
        catalog_state.remove_catalog(catalog_name)
        console.print(f'🗑️  Removed catalog "{catalog_name}"', style='yellow')
    except Exception as e:
        console.print(f'❌ Error removing catalog: {e}', style='bold red')
        raise typer.Exit(1) from e
