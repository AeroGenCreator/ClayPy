import importlib


class ClayPyShell:

    def __init__(self, container, page):
        super().__init__()
        # Aqui agrego el contendor con la vista.
        self.container = container
        self.page = page

    def view_extraction(self, route, view):
        """
        Carga la vista principal en el contenedor.
        Depende de la ruta a la vista principal del modulo por evaluar.
        """
        module = importlib.import_module(route)
        View = getattr(module, view, None)

        if View is None:
            raise ValueError(
                "Following path does not contain a Flet 'view'. "
                f"{module}. Make sure 'View' class exist."
            )

        view = View()
        self.container.content = view.build()
        self.page.update()
