import os
import typer
from deltacat_cli.namespace.alter import app as alter_app, alter_namespace_cmd
from deltacat_cli.config import console, err_console


app = typer.Typer(name='Namespace')

@app.callback()
def namespace_callback(ctx: typer.Context) -> None:
    """
    Namespace operations for DeltaCat.
    
    All namespace commands require a catalog to be configured first.
    Use 'deltacat catalog init initialize' or 'deltacat catalog set' to configure a catalog.
    """
    # All namespace commands require a catalog to be set
    catalog_name = os.environ.get('DELTACAT_CLI_CATALOG_NAME')
    catalog_root = os.environ.get('DELTACAT_CLI_CATALOG_ROOT')
    
    if not catalog_name or not catalog_root:
        err_console.print('❌ No catalog configured in this session.', style='bold red')
        console.print('Set catalog with: [bold cyan]deltacat catalog set[/bold cyan] or [bold cyan]deltacat catalog init initialize[/bold cyan]')
        raise typer.Exit(1)

# Extract docstrings from the actual command functions
app.add_typer(alter_app, name='alter', help=alter_namespace_cmd.__doc__)