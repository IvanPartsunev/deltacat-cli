from deltacat import Catalog, CatalogProperties, put_catalog


def initialize_catalog(root: str, catalog_name: str) -> CatalogProperties:
    """Initializes the deltacat catalog for the database."""
    root = f'{root}/{catalog_name}'
    catalog = CatalogProperties(root=root)
    catalog_obj = Catalog(config=catalog)
    put_catalog(catalog_name, catalog_obj)

    return catalog
