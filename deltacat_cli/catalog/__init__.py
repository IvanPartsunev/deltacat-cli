import typer

from deltacat_cli.catalog.clear import clear_catalog
from deltacat_cli.catalog.context import catalog_context
from deltacat_cli.catalog.current import show_catalog
from deltacat_cli.catalog.init import initialize
from deltacat_cli.catalog.set import set_catalog


app = typer.Typer(name='Catalog')


@app.callback()
def catalog_callback(ctx: typer.Context) -> None:
    """Catalog operations for DeltaCat.

    Commands that require a catalog (like 'current') will check for environment variables.
    Use 'init' or 'set' commands to configure a catalog first.
    """
    # Commands that don't require a catalog to be set
    commands_without_catalog = {'init', 'set'}

    # Get the command being executed
    if ctx.invoked_subcommand and ctx.invoked_subcommand not in commands_without_catalog:
        # Check if catalog is configured - will raise typer.Exit if not configured
        catalog_context.get_catalog_info()


# Add commands directly (no nested structure)
app.command(name='init', help=initialize.__doc__)(initialize)
app.command(name='set', help=set_catalog.__doc__)(set_catalog)
app.command(name='current', help=show_catalog.__doc__)(show_catalog)
app.command(name='clear', help=clear_catalog.__doc__)(clear_catalog)
