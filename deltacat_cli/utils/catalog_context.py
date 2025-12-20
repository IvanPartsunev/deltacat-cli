"""Simple catalog context management."""

import json
from pathlib import Path

import typer

from deltacat import Catalog, CatalogProperties, put_catalog
from deltacat_cli.config import CONFIG_ERROR_MODE, console, err_console


class CatalogContext:
    """Simple catalog context using environment variables and file persistence."""

    def __init__(self):
        self._cached_catalog: Catalog | None = None
        self._cached_name: str | None = None
        self._cached_root: str | None = None
        self._config_file = Path.home() / '.deltacat_cli_config.json'

    def set_catalog(self, name: str, root: str) -> None:
        """Set the current catalog and persist to file."""
        # Persist to file
        self._save_config({'name': name, 'root': root})

        # Clear cache when setting new catalog
        self._clear_cache()
        console.print(f'Catalog [bold]set[/bold] to: [bold blue]{name}[/bold blue]', style='green')
        console.print(f'Root: {root}', style='dim')
        console.print(f'Full path: {root}/{name}', style='dim')

    def get_catalog_info(self) -> tuple[str, str]:
        """Get current catalog name and root, or raise error if not set."""
        config = self._load_config()

        if not config:
            err_console.print('No catalog configured.', style='bold red')
            console.print(
                'Set catalog with: [bold cyan]deltacat catalog set[/bold cyan] or [bold cyan]deltacat catalog init[/bold cyan]'
            )
            raise typer.Exit(1)

        name = config.get('name')
        root = config.get('root')

        if not name or not root:
            err_console.print('Invalid catalog configuration.', style='bold red')
            console.print(
                'Set catalog with: [bold cyan]deltacat catalog set[/bold cyan] or [bold cyan]deltacat catalog init[/bold cyan]'
            )
            raise typer.Exit(1)

        console.print(f'Current catalog: [bold blue]{name}[/bold blue]', style='green')
        console.print(f'Root: {root}', style='dim')
        console.print(f'Full path: {root}/{name}', style='dim')

        return name, root

    def get_catalog(self) -> Catalog:
        """Get the current catalog instance (cached)."""
        name, root = self.get_catalog_info()

        # Return cached if same catalog
        if self._cached_catalog and self._cached_name == name and self._cached_root == root:
            return self._cached_catalog

        # Try to get from deltacat registry first
        # Always create and register the catalog since each command runs in a new process
        catalog_props = CatalogProperties(root=f'{root}/{name}')
        self._cached_catalog = Catalog(config=catalog_props)

        put_catalog(name, self._cached_catalog)

        self._cached_name = name
        self._cached_root = root
        return self._cached_catalog

    def clear_catalog(self) -> None:
        """Clear the current catalog configuration."""
        # Remove config file
        if self._config_file.exists():
            self._config_file.unlink()

        self._clear_cache()
        console.print('Catalog configuration cleared', style='bold yellow')

    def _clear_cache(self) -> None:
        """Clear the cached catalog."""
        self._cached_catalog = None
        self._cached_name = None
        self._cached_root = None

    def _save_config(self, config: dict) -> None:
        """Save configuration to file."""
        try:
            with open(self._config_file, 'w') as f:
                json.dump(config, f)
        except OSError as e:
            if CONFIG_ERROR_MODE == 'strict':
                err_console.print(f'Error: Could not save config to {self._config_file}: {e}', style='bold red')
                raise typer.Exit(1) from e
            if CONFIG_ERROR_MODE == 'warn':
                console.print(f'Warning: Could not save config to {self._config_file}: {e}', style='yellow')
                console.print('   Configuration will not persist between sessions.', style='dim')

    def _load_config(self) -> dict | None:
        """Load configuration from file."""
        try:
            if self._config_file.exists():
                with open(self._config_file) as f:
                    return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            if CONFIG_ERROR_MODE == 'strict':
                err_console.print(f'Error: Could not load config from {self._config_file}: {e}', style='bold red')
                raise typer.Exit(1) from e
            if CONFIG_ERROR_MODE == 'warn':
                console.print(f'Warning: Could not load config from {self._config_file}: {e}', style='yellow')
                console.print('   You may need to reconfigure your catalog.', style='dim')
        return None


catalog_context = CatalogContext()
