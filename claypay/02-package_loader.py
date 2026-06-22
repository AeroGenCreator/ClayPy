"""
Carga interactiva de modulos.

Se carga:
1. Boton para barra lateral. Accion de menu principal.
2. Carga de los NavigationBarItem's
3. Modelos para poder ejecutarlos.
"""

import importlib
from pathlib import Path

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
        container_items.update({NAME: CONTAINER_ITEMS})
        sidebar_button.update({NAME: SIDEBAR_BUTTON})
        dynamic_models.extend(DYNAMIC_MODELS)

    print(container_items)
    print(sidebar_button)
    print(dynamic_models)

read_manifest()
