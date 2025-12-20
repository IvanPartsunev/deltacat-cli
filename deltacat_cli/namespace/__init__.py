import typer

from deltacat_cli.namespace.alter import app as alter_app
from deltacat_cli.namespace.create import app as creat_app


app = typer.Typer()

app.add_typer(alter_app)
app.add_typer(creat_app)
