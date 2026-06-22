from claypay.dataclasses import NavigationBarItem

from ..backend.expose_models import get_categories, get_inventory

inventory_kwargs = {
    "function": get_inventory,
    "name": "Inventario",
    "key": "inventory"
}
category_kwargs = {
    "function": get_categories,
    "name": "Categorias",
    "key": "category"
}

inventory = NavigationBarItem(**inventory_kwargs)
category = NavigationBarItem(**category_kwargs)
