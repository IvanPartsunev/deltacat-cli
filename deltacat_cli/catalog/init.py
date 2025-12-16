import typer
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from deltacat_cli.catalog.operations import initialize_catalog
from deltacat_cli.config import console


app = typer.Typer()

@app.command()
def initialize() -> None:
    """Initialize a new DeltaCat catalog."""
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