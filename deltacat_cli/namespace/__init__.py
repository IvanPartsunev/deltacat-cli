import typer

from deltacat_cli.namespace.alter import app as alter_app
from deltacat_cli.namespace.create import app as creat_app
from deltacat_cli.namespace.drop import app as drop_app
from deltacat_cli.namespace.list import app as list_app
from deltacat_cli.namespace.get import app as get_app


app = typer.Typer()

app.add_typer(alter_app)
app.add_typer(creat_app)
app.add_typer(drop_app)
app.add_typer(list_app)
app.add_typer(get_app)
