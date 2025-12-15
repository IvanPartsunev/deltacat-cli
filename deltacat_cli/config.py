import typer
from rich.console import Console
from rich.spinner import SPINNERS


# Register custom spinner
SPINNERS['cat'] = {
    'frames': ['😸', '😺', '😼'],
    'interval': 300,
}

app = typer.Typer(
    name='deltacat-cli',
    help='A CLI application for working with deltacat',
    add_completion=False,
)

console = Console()
err_console = Console(stderr=True)
