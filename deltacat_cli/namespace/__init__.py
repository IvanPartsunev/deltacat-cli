import typer

from deltacat_cli.namespace.alter import alter_namespace_cmd
from deltacat_cli.namespace.create import create_namespace_cmd


app = typer.Typer(name='Namespace')

app.command(name='alter', help=alter_namespace_cmd.__doc__)(alter_namespace_cmd)
app.command(name='create', help=create_namespace_cmd.__doc__)(create_namespace_cmd)
