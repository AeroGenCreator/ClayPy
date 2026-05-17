import importlib


class ClayPyShell:

    def __init__(self, container, page):
        super().__init__()
        self.container = container
        self.page = page

    def view_extraction(self, route, view):
        module = importlib.import_module(route)
        VIEW = getattr(module, view, None)

        if VIEW is None:
            raise ValueError(
                "Following path does not contain a Flet 'view'. "
                f"{module}. Make sure 'View' class exist."
            )

        view = VIEW()
        self.container.content = view.build()
        self.page.update()
