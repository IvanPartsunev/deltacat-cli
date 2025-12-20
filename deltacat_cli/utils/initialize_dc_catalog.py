from deltacat import Catalog, CatalogProperties, put_catalog
from deltacat_cli.utils.catalog_context import catalog_context


def initialize_catalog(root: str, catalog_name: str) -> CatalogProperties:
  """Initialize the deltacat catalog and set as current."""
  full_root = f'{root}/{catalog_name}'
  catalog = CatalogProperties(root=full_root)
  catalog_obj = Catalog(config=catalog)
  put_catalog(catalog_name, catalog_obj)

  catalog_context.set_catalog(catalog_name, root)

  return catalog
