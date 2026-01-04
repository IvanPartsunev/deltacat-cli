from rich.console import Console


console = Console()
err_console = Console(stderr=True)

# Configure Typer to show full tracebacks in development
# Set to False in production for cleaner error messages
SHOW_TRACEBACK = True

# Config file error handling mode
CONFIG_ERROR_MODE = 'warn'  # 'silent', 'warn', 'strict'

# Configure Typer to show full tracebacks in development
# Set to False in production for cleaner error messages
SHOW_TRACEBACK = True

# Config file error handling mode
CONFIG_ERROR_MODE = 'warn'  # 'silent', 'warn', 'strict'
