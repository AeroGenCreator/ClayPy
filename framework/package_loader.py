import importlib
from pathlib import Path

PATH = Path().cwd()
PATH = PATH / "packages"


def package_loader(path=PATH):

    # Determina rutas __manifest__.py
    paths = {}
    for package in path.iterdir():
        for file in package.iterdir():
            if file.name == "__manifest__.py":
                paths.update(
                    {package.name: f"packages.{package.name}.__manifest__"}
                )

    loaded_metadata = {}

    for name, route in paths.items():
        module = importlib.import_module(route)
        dicc = module.PACKAGE
        loaded_metadata.update({name: dicc})

    return loaded_metadata
