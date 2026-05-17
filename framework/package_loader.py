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

    loaded_menu = {}
    loaded_view = {}
    loaded_models = []

    for name, route in paths.items():
        module = importlib.import_module(route)
        dicc = module.PACKAGE

        MENU = dicc.get("menu", None)
        VIEW = dicc.get("view", None)
        MODELS = dicc.get("models", None)

        validate = ((MENU is None), (VIEW is None), (MODELS is None))

        if any(validate):
            raise KeyError(
                f"Missing kewys; Manifest '{name}', Metadata '{dicc}' "
                "Valid keys are; 'menus', 'views', 'models'."
            )

        loaded_menu.update({name: MENU})
        loaded_view.update({name: VIEW})
        loaded_models.extend(MODELS)

    return loaded_menu, loaded_view, loaded_models

def run_models(models_pack):
    for dicc in models_pack:
        for model, route in dicc.items():
            module = importlib.import_module(route)
            CLAS = getattr(module, model, None)

            if CLAS is None:
                raise ValueError
