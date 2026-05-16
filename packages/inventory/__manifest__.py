# Prometheus default __manifest__.py

PACKAGE = {
    "name": "inventory",
    "menus": [
        {
        "label": "Inventario",
        "route": "inventory.table",
        "icons": "all_inbox"
        },
        {
        "label": "Ajustes",
        "route": "Inventario.ajustes",
        "icons": "settings"
        }
    ],
    "views": {"inventory.table": "InventoryTable"}
}
