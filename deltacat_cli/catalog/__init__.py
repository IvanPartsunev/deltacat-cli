import typer

from deltacat_cli.catalog.clear import clear_catalog
from deltacat_cli.catalog.current import show_catalog
from deltacat_cli.catalog.init import initialize
from deltacat_cli.catalog.set import set_catalog


app = typer.Typer(name='Catalog')

# Add commands directly (no nested structure)
app.command(name='init', help=initialize.__doc__)(initialize)
app.command(name='set', help=set_catalog.__doc__)(set_catalog)
app.command(name='current', help=show_catalog.__doc__)(show_catalog)
app.command(name='clear', help=clear_catalog.__doc__)(clear_catalog)
