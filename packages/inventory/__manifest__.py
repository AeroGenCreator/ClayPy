PACKAGE = {
    "name": "inventory",
    "menu":
        {
        "label": "Inventario",
        "route": "packages.inventory",
        "icons": "all_inbox"
        },
    "view": {
        "path": "packages.inventory.views.main_view",
        "class": "View"
        },
    "models": [
        {
        "Inventory": "packages.inventory.models.inventory",
        "Categories": "packages.inventory.models.categories"
        }
    ]
}
