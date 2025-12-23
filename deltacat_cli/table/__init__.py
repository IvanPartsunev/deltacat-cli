import typer

from deltacat_cli.table.create import app as create_app
from deltacat_cli.table.get import app as get_app


app = typer.Typer()


app.add_typer(get_app)
app.add_typer(create_app)
