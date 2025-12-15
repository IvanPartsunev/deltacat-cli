"""Catalog state management for deltacat-cli."""

import json
from pathlib import Path

import typer

from deltacat_cli.config import console


class CatalogState:
    """Manages catalog state and configuration."""

    def __init__(self):
        self.config_dir = Path.home() / '.deltacat-cli'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(exist_ok=True)
        self._config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {'catalogs': {}, 'current_catalog': None}
        return {'catalogs': {}, 'current_catalog': None}

    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except OSError as e:
            console.print(f'❌ Error saving config: {e}', style='bold red')

    def add_catalog(self, name: str, root: str) -> None:
        """Add a new catalog configuration."""
        self._config['catalogs'][name] = {'name': name, 'root': root}

        # Set as current if it's the first catalog
        if not self._config['current_catalog']:
            self._config['current_catalog'] = name

        self._save_config()
        console.print(f'✅ Catalog "{name}" added to configuration', style='green')

    def set_current_catalog(self, name: str) -> None:
        """Set the current active catalog."""
        if name not in self._config['catalogs']:
            raise typer.BadParameter(f'Catalog "{name}" not found')

        self._config['current_catalog'] = name
        self._save_config()
        console.print(f'✅ Current catalog set to "{name}"', style='green')

    def get_current_catalog(self) -> dict | None:
        """Get the current active catalog configuration."""
        current_name = self._config['current_catalog']
        if not current_name:
            return None

        return self._config['catalogs'].get(current_name)

    def get_catalog(self, name: str) -> dict | None:
        """Get a specific catalog configuration."""
        return self._config['catalogs'].get(name)

    def list_catalogs(self) -> dict:
        """List all configured catalogs."""
        return self._config['catalogs']

    def remove_catalog(self, name: str) -> None:
        """Remove a catalog configuration."""
        if name not in self._config['catalogs']:
            raise typer.BadParameter(f'Catalog "{name}" not found')

        del self._config['catalogs'][name]

        # If this was the current catalog, clear it
        if self._config['current_catalog'] == name:
            # Set to another catalog if available
            remaining = list(self._config['catalogs'].keys())
            self._config['current_catalog'] = remaining[0] if remaining else None

        self._save_config()
        console.print(f'✅ Catalog "{name}" removed', style='green')

    def require_current_catalog(self) -> dict:
        """Get current catalog or raise error if none set."""
        current = self.get_current_catalog()
        if not current:
            console.print('❌ No catalog is currently active.', style='bold red')
            console.print(
                'Initialize a catalog first with: [bold cyan]deltacat-cli catalog init[/bold cyan]'
            )
            raise typer.Exit(1)
        return current


# Global state instance
catalog_state = CatalogState()
