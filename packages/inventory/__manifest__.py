# Prometheus default __manifest__.py

PACKAGE = {
    "name": "inventory",
    "menus": [
        {
        "label": "Inventario",
        "route": "inventory.views.inventory_table",
        "icons": "all_inbox"
        }
    ],
    "views": {"inventory.table": "InventoryTable"}
}
