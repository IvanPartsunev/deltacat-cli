from deltacat import Catalog, CatalogProperties, put_catalog

from deltacat_cli.catalog.state import catalog_state


def initialize_catalog(root: str, catalog_name: str) -> CatalogProperties:
    """Initialize the deltacat catalog and save to state."""
    full_root = f'{root}/{catalog_name}'
    catalog = CatalogProperties(root=full_root)
    catalog_obj = Catalog(config=catalog)
    put_catalog(catalog_name, catalog_obj)

    # Save to state management
    catalog_state.add_catalog(catalog_name, full_root)

    return catalog


def get_current_catalog() -> Catalog:
    """Get the current active catalog instance."""
    current = catalog_state.require_current_catalog()
    catalog_props = CatalogProperties(root=current['root'])
    return Catalog(config=catalog_props)
