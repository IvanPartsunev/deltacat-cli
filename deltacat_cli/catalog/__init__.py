import typer

from deltacat_cli.catalog.clear import app as clear_app
from deltacat_cli.catalog.init import app as initialize_app
from deltacat_cli.catalog.set import app as set_app
from deltacat_cli.catalog.show import app as show_app


app = typer.Typer()

app.add_typer(initialize_app)
app.add_typer(set_app)
app.add_typer(show_app)
app.add_typer(clear_app)
