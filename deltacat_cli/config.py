import typer
from rich.console import Console
from rich.spinner import SPINNERS


# Register custom spinner
SPINNERS['cat'] = {'frames': ['😸', '😺', '😼'], 'interval': 300}

console = Console()
err_console = Console(stderr=True)

# Configure Typer to show full tracebacks in development
# Set to False in production for cleaner error messages
SHOW_TRACEBACK = True
