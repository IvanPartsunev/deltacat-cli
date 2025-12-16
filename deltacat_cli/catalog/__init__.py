import typer
from deltacat_cli.catalog.clear import app as clear_app
from deltacat_cli.catalog.current import app as current_app
from deltacat_cli.catalog.init import app as init_app
from deltacat_cli.catalog.set import app as set_app


app = typer.Typer(name='Catalog')

app.add_typer(init_app, name='init')
app.add_typer(set_app, name='set')
app.add_typer(current_app, name='current')
app.add_typer(clear_app, name='clear')
