"""Common error handlers for CLI commands."""

import typer
from deltacat_cli.config import console, err_console
from deltacat_cli.utils.emojis import get_emoji


def handle_catalog_error(e: Exception, operation: str) -> None:
    """Handle common catalog-related errors with user-friendly messages.
    
    Args:
        e: The exception that was raised
        operation: Description of the operation being performed (e.g., "creating namespace")
    """
    if isinstance(e, ValueError) and "No catalogs available" in str(e) and "deltacat.init" in str(e):
        err_console.print(f'{get_emoji("error")} No catalog configured or available', style='bold red')
        console.print(
            'Set catalog with: [bold cyan]deltacat catalog set[/bold cyan] or [bold cyan]deltacat catalog init[/bold cyan]'
        )
        raise typer.Exit(1) from e
    else:
        err_console.print(f'{get_emoji("error")} Error {operation}: {e}', style='bold red')
        raise typer.Exit(1) from e