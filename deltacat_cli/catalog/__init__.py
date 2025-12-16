import typer
from deltacat_cli.catalog.clear import app as clear_app
from deltacat_cli.catalog.current import app as current_app
from deltacat_cli.catalog.init import app as init_app
from deltacat_cli.catalog.set import app as set_app


app = typer.Typer(name='Catalog')

app.add_typer(init_app, name='init', help='Initialize a new DeltaCat catalog')
app.add_typer(set_app, name='set', help='Set the current catalog for this session')
app.add_typer(current_app, name='current', help='Show the current active catalog')
app.add_typer(clear_app, name='clear', help='Clear the current catalog configuration')
