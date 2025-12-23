import json
from typing import Any, Literal

from rich.panel import Panel
from rich.syntax import Syntax

from deltacat_cli.config import console


def print_as_json(source_type: Literal['namespace', 'table'], data: dict[Any, Any]) -> None:
    """Print dict as json."""
    json_str = json.dumps(data, indent=2, default=str)
    syntax = Syntax(json_str, 'json', theme='github-dark', line_numbers=False, word_wrap=True)
    panel = Panel(
        syntax,
        title=f'[bold green]{source_type.capitalize()}[/bold green]',
        border_style='blue',
        title_align='left',
        padding=(0, 1),
    )

    console.print(panel)
    console.print()
