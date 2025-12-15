from rich.console import Console
from rich.spinner import SPINNERS


# Register custom spinner
SPINNERS['cat'] = {'frames': ['😸', '😺', '😼'], 'interval': 300}

console = Console()
err_console = Console(stderr=True)
