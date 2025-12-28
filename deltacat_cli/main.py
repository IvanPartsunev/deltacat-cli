"""Main CLI application for deltacat."""

import typer
from rich import print as rich_print

from deltacat_cli import __version__
from deltacat_cli.catalog import app as catalog_app
from deltacat_cli.config import SHOW_TRACEBACK, err_console
from deltacat_cli.namespace import app as namespace_app
from deltacat_cli.table import app as table_app
from deltacat_cli.utils.catalog_context import catalog_context
from deltacat_cli.utils.emojis import EMOJI_SETS, get_emoji, set_emoji_style


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        rich_print(f'deltacat version: {__version__}')
        raise typer.Exit(0)


app = typer.Typer(
    name='deltacat',
    help='A CLI application for working with deltacat',
    add_completion=True,
    pretty_exceptions_enable=not SHOW_TRACEBACK,
    pretty_exceptions_show_locals=SHOW_TRACEBACK,
)


@app.callback()
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(  # noqa: ARG001
        False,  # noqa: FBT003
        '--version',
        '-v',
        callback=version_callback,
        is_eager=True,
        help='Show version and exit',
    ),
) -> None:
    """DeltaCat CLI - A command-line interface for working with deltacat.

    Use 'deltacat catalog init' to get started.
    """
    if ctx.invoked_subcommand:
        commands_without_catalog = {'catalog'}

        if ctx.invoked_subcommand not in commands_without_catalog:
            catalog_context.get_catalog_info(silent=True)


# @app.command()
# def emoji_style(
#     style: str = typer.Argument(None, help='Emoji style: professional, geometric, minimal, colorful'),
#     show: bool = typer.Option(False, '--show', help='Show available emoji styles'),
# ) -> None:
#     """Change emoji style for CLI output."""
#     if show:
#         rich_print('[bold yellow]Available emoji styles:[/bold yellow]\n')
#         for style_name, emojis in EMOJI_SETS.items():
#             rich_print(f'[bold cyan]{style_name}:[/bold cyan]')
#             rich_print(
#                 f'  {emojis["loading"]} loading  {emojis["success"]} success  {emojis["error"]} error  {emojis["warning"]} warning'
#             )
#             rich_print()
#         return

# if not style:
#     rich_print('[red]Please specify a style or use --show to see available styles[/red]')
#     raise typer.Exit(1)
#
# if style not in EMOJI_SETS:
#     rich_print(f'[red]Unknown style: {style}[/red]')
#     rich_print(f'Available styles: {", ".join(EMOJI_SETS.keys())}')
#     raise typer.Exit(1)
#
# set_emoji_style(style)
# rich_print(f'{get_emoji("success")} Emoji style changed to: [bold cyan]{style}[/bold cyan]')


app.add_typer(catalog_app, name='catalog', help='Catalog operations for DeltaCat')
app.add_typer(namespace_app, name='namespace', help='Namespace operations for DeltaCat')
app.add_typer(table_app, name='table', help='Table operations for DeltaCat')


def main() -> None:
    """Entry point for the CLI application."""
    try:
        app()
    except Exception as e:
        if SHOW_TRACEBACK:
            raise
        err_console.print(f'{get_emoji("error")} Error: {e}', style='bold red')
        raise typer.Exit(1) from e
