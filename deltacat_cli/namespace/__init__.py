import typer

from deltacat_cli.catalog.context import catalog_context
from deltacat_cli.namespace.alter import alter_namespace_cmd
from deltacat_cli.namespace.create import create_namespace_cmd


app = typer.Typer(name='Namespace')


@app.callback()
def namespace_callback() -> None:
    """Namespace operations for DeltaCat.

    All namespace commands require a catalog to be configured first.
    Use 'deltacat catalog init initialize' or 'deltacat catalog set' to configure a catalog.
    """
    # All namespace commands require a catalog to be set
    # This will raise typer.Exit(1) if no catalog is configured
    catalog_context.get_catalog_info()


# Add commands directly (no nested structure)
app.command(name='alter', help=alter_namespace_cmd.__doc__)(alter_namespace_cmd)
app.command(name='create', help=create_namespace_cmd.__doc__)(create_namespace_cmd)
