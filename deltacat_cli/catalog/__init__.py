import typer
from clear import app as clear_app
from current import app as current_app
from init import app as init_app
from set import app as set_app


app = typer.Typer(name='Catalog')

app.add_typer(init_app, name='init')
app.add_typer(set_app, name='set')
app.add_typer(current_app, name='set')
app.add_typer(clear_app, name='set')
