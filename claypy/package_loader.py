"""
Carga interactiva de modulos.

Se carga:
1. Boton para barra lateral. Accion de menu principal.
2. Carga de los NavigationBarItem's
3. Modelos para poder ejecutarlos.
"""

# Modulos Python
import importlib
from pathlib import Path

# Modulos Terceros
import flet as ft

# La ruta aqui es estatica. Modificar para ser leida desde un .env
IMPORT_COMPLEMENT = "packages"
PATH = Path.cwd() / IMPORT_COMPLEMENT
MANIFEST_KEY_WORD = "__manifest__.py"
METADATA_KEY_WORD = "PACKAGE"


def read_manifest(path=PATH):

    # Guarda: Nombre Directorio / Ruta Importación Al Manifest Python
    manifest = {}

    for directory in path.iterdir():
        for file in directory.iterdir():
            if file.name == MANIFEST_KEY_WORD:
                line = f"{IMPORT_COMPLEMENT}.{directory.name}.__manifest__"
                manifest.update({directory.name: line})

    # Importacion de cada __manifest__ por paquete declarado.
    container_items = {}
    sidebar_button = {}
    dynamic_models = []

    # Se importa el modulo y se accede al diccionario del __manifest__
    for directory_name, manifest_path in manifest.items():
        module = importlib.import_module(manifest_path)
        metadata = getattr(module, METADATA_KEY_WORD, None)

        if metadata is None:
            raise ValueError("Error while accessing manifest metadata.")

        # Extraccion de parametros de paquetes.
        CONTAINER_ITEMS = metadata.get("container", None)
        DYNAMIC_MODELS = metadata.get("models", None)
        SIDEBAR_BUTTON = metadata.get("menu", None)
        NAME = metadata.get("name", None)

        # Validar que todo contenga data.
        validate = (
            (CONTAINER_ITEMS is None),
            (DYNAMIC_MODELS is None),
            (SIDEBAR_BUTTON is None),
            (NAME is None),
        )

        if any(validate):
            raise ValueError("Error, no data extracted in metadata.")

        # Creacion de diccionarios etiquetados.

        # === {"Paquete": {"ruta": ["instancias", ...]}} ===
        container_items.update({NAME: CONTAINER_ITEMS})
        # === {"Paquete": {kwargs}} ===
        sidebar_button.update({NAME: SIDEBAR_BUTTON})
        # === {"Modelo": "ruta"} ===
        dynamic_models.extend(DYNAMIC_MODELS)

    # Se retornan las lecturas separadas
    return container_items, sidebar_button, dynamic_models


def load_models(models_list: list):
    """
    Ejemplo de lista de modelos. Leido desde el __manifest__.py
    [
        {
            'Inventory': 'packages.inventory.models.inventory',
            'Category': 'packages.inventory.models.category'
        }
    ]
    """
    # Iterar diccionarios de la lista.
    for dictionary in models_list:
        # Para cada diccionario importar los modelos.
        for class_name, path in dictionary.items():
            module = importlib.import_module(path)
            CLASS = getattr(module, class_name, None)
            # Si alguna ruta no se resuleve, mostrar error.
            if CLASS is None:
                raise(
                    f"Cannot import the following model: {class_name}."
                    "Make sure to be specific with the route and the class."
                )

def content_constructor():
    """
    Ejemplo de ruta a las instancias de "topbar" - "contenido respuesta"
    {
        'inventory': {
            'packages.inventory.views.items': [
                'inventory', 'category'
            ]
        }
    }
    Debe retornar una lista de contenidos para contenedor.
    Ejemplo: [{"paquete": {"item_1": flet.Contenido, "item_2": flet.Contenido}}]
    """
    pass

def sidebar_button_constructor():
    """
    {
        'inventory': {
            'label': 'Inventario',
            'route': 'packages.inventory',
            'icons': 'all_inbox'
        }
    }
    """
    pass
