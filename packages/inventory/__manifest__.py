PACKAGE = {
    "name": "inventory",
    "menu":
        {
        "label": "Inventario",
        "route": "packages.inventory",
        "icons": "all_inbox"
        },
    "container": {
        "packages.inventory.views.items": ["inventory", "category"]
        },
    "models": [
        {
        "Inventory": "packages.inventory.models.inventory",
        "Category": "packages.inventory.models.category"
        },
    ]
}
