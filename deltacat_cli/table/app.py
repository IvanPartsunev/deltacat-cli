"""Table management commands."""

import typer

from deltacat_cli.catalog.operations import get_current_catalog
from deltacat_cli.catalog.state import catalog_state
from deltacat_cli.config import console


app = typer.Typer(name='Table')


@app.command()
def list() -> None:
    """List all tables in the current catalog."""
    # Get current catalog (will exit if none set)
    current = catalog_state.require_current_catalog()
    console.print(f'📋 Tables in catalog "[bold green]{current["name"]}[/bold green]":')

    try:
        catalog = get_current_catalog()
        # TODO: Implement actual table listing with deltacat
        console.print('   (Table listing not yet implemented)', style='dim')
        console.print(f'   Catalog root: {current["root"]}', style='dim')
    except Exception as e:
        console.print(f'❌ Error listing tables: {e}', style='bold red')
        raise typer.Exit(1) from e


@app.command()
def create(table_name: str) -> None:
    """Create a new table in the current catalog."""
    current = catalog_state.require_current_catalog()
    console.print(
        f'🔨 Creating table "[bold cyan]{table_name}[/bold cyan]" '
        f'in catalog "[bold green]{current["name"]}[/bold green]"'
    )

    try:
        catalog = get_current_catalog()
        # TODO: Implement actual table creation with deltacat
        console.print('   (Table creation not yet implemented)', style='dim')
        console.print(f'   Would create in: {current["root"]}', style='dim')
    except Exception as e:
        console.print(f'❌ Error creating table: {e}', style='bold red')
        raise typer.Exit(1) from e


@app.command()
def info(table_name: str) -> None:
    """Show information about a table."""
    current = catalog_state.require_current_catalog()
    console.print(
        f'ℹ️  Table "[bold cyan]{table_name}[/bold cyan]" in catalog "[bold green]{current["name"]}[/bold green]":'
    )

    try:
        catalog = get_current_catalog()
        # TODO: Implement actual table info with deltacat
        console.print('   (Table info not yet implemented)', style='dim')
        console.print(f'   Catalog root: {current["root"]}', style='dim')
    except Exception as e:
        console.print(f'❌ Error getting table info: {e}', style='bold red')
        raise typer.Exit(1) from e
