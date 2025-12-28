import typer

from deltacat_cli.table.create import app as create_app
from deltacat_cli.table.get import app as get_app
from deltacat_cli.table.drop import app as drop_app
from deltacat_cli.table.alter import app as alter_app


app = typer.Typer()


app.add_typer(get_app)
app.add_typer(create_app)
app.add_typer(drop_app)
app.add_typer(alter_app)
