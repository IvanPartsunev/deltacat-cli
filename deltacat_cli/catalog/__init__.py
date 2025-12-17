import os
import typer
from deltacat_cli.catalog.clear import app as clear_app, clear_catalog
from deltacat_cli.catalog.current import app as current_app, show_catalog
from deltacat_cli.catalog.init import app as init_app, initialize
from deltacat_cli.catalog.set import app as set_app, set_catalog
from deltacat_cli.config import console, err_console


app = typer.Typer(name='Catalog')

@app.callback()
def catalog_callback(ctx: typer.Context) -> None:
    """
    Catalog operations for DeltaCat.
    
    Commands that require a catalog (like 'current') will check for environment variables.
    Use 'init' or 'set' commands to configure a catalog first.
    """
    # Commands that don't require a catalog to be set
    commands_without_catalog = {'init', 'set'}
    
    # Get the command being executed
    if ctx.invoked_subcommand and ctx.invoked_subcommand not in commands_without_catalog:
        # Check if catalog environment variables are set
        catalog_name = os.environ.get('DELTACAT_CLI_CATALOG_NAME')
        catalog_root = os.environ.get('DELTACAT_CLI_CATALOG_ROOT')
        
        if not catalog_name or not catalog_root:
            err_console.print('❌ No catalog configured in this session.', style='bold red')
            console.print('Set catalog with: [bold cyan]deltacat catalog set[/bold cyan] or [bold cyan]deltacat catalog init initialize[/bold cyan]')
            raise typer.Exit(1)

# Extract docstrings from the actual command functions
app.add_typer(init_app, name='init', help=initialize.__doc__)
app.add_typer(set_app, name='set', help=set_catalog.__doc__)
app.add_typer(current_app, name='current', help=show_catalog.__doc__)
app.add_typer(clear_app, name='clear', help=clear_catalog.__doc__)
