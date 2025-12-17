"""Simple catalog context management."""

import os

import typer
from deltacat import Catalog, CatalogProperties

from deltacat_cli.config import console, err_console


class CatalogContext:
    """Simple catalog context using environment variables."""

    def __init__(self):
        self._cached_catalog: Catalog | None = None
        self._cached_name: str | None = None
        self._cached_root: str | None = None

    def set_catalog(self, name: str, root: str) -> None:
        """Set the current catalog via environment variables."""
        os.environ['DELTACAT_CLI_CATALOG_NAME'] = name
        os.environ['DELTACAT_CLI_CATALOG_ROOT'] = root
        # Clear cache when setting new catalog
        self._clear_cache()
        console.print(f'✅ Catalog set to "{name}" at "{root}"', style='green')

    def get_catalog_info(self) -> tuple[str, str]:
        """Get current catalog name and root, or raise error if not set."""
        name = os.environ.get('DELTACAT_CLI_CATALOG_NAME')
        root = os.environ.get('DELTACAT_CLI_CATALOG_ROOT')

        if not name or not root:
            err_console.print('❌ No catalog configured in this session.', style='bold red')
            console.print('Set catalog with: [bold cyan]deltacat catalog set[/bold cyan]')
            raise typer.Exit(1)

        return name, root

    def get_catalog(self) -> Catalog:
        """Get the current catalog instance (cached)."""
        name, root = self.get_catalog_info()

        # Return cached if same catalog
        if self._cached_catalog and self._cached_name == name and self._cached_root == root:
            return self._cached_catalog

        # Create and cache new catalog
        catalog_props = CatalogProperties(root=f'{root}/{name}')
        self._cached_catalog = Catalog(config=catalog_props)
        self._cached_name = name
        self._cached_root = root

        return self._cached_catalog

    def clear_catalog(self) -> None:
        """Clear the current catalog configuration."""
        os.environ.pop('DELTACAT_CLI_CATALOG_NAME', None)
        os.environ.pop('DELTACAT_CLI_CATALOG_ROOT', None)
        self._clear_cache()
        console.print('✅ Catalog configuration cleared', style='yellow')

    def _clear_cache(self) -> None:
        """Clear the cached catalog."""
        self._cached_catalog = None
        self._cached_name = None
        self._cached_root = None


# Global context instance
catalog_context = CatalogContext()
