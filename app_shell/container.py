import flet as ft


class MainContainer(ft.Container):
    """
    Clase contenedor principal; pensado para poder editar
    parametros de manera dinamica y controlada.
    Asi mismo acceso direco a .content="vista" para carga de paquetes.
    """

    def __init__(self, content):
        super().__init__()
        self.content = content
        self.expand = 11
        self.padding = 20
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
        self.border_radius = 10
        self.alignment = ft.Alignment.CENTER
