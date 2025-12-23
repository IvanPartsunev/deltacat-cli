import json
from typing import Any, Literal

from rich.panel import Panel
from rich.syntax import Syntax

from deltacat_cli.config import console


def print_json(source_type: Literal['namespace', 'table'], data: dict[Any, Any]):
    json_str = json.dumps(data, indent=2, default=str)
    syntax = Syntax(json_str, 'json', theme='dracula', line_numbers=False)
    panel = Panel(
        syntax,
        title=f'[bold green]{source_type.capitalize()}[/bold green]',
        border_style='blue',
        title_align='left',
        padding=(0, 0),
    )

    console.print(panel)
    console.print()
