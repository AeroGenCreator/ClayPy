import flet as ft


class Sidebar(ft.Column):
    """
    Construccion de sidebar;
    Se inyecta la metadata de los paquetes (__manifest__)
    Construccion dinamica de botones y rutas de navegacion.
    """

    def __init__(
        self,
        menu,
        view,
        shell,
        app_page: ft.Page
    ):
        super().__init__()
        # Variables de construccion
        self.menu = menu
        self.view = view
        self.shell = shell
        self.app_page = app_page
        # Atributos heredados
        self.bgcolor = ft.Colors.BLUE_GREY_900
        self.alignment = ft.MainAxisAlignment.START
        self.spacing = 10
        self.wrap = False
        self.expand = False
        self.width = 225
        self.intrinsic_width = False
        # Boton de cerrar sesion 'Pendiente'
        self.logout = ft.TextButton(
            content="Cerrar Sesion",
            icon=ft.Icons.ARROW_BACK,
            style=ft.ButtonStyle(
                        bgcolor={"": "#4a2222"},
                        color={"": ft.Colors.WHITE}
                    )
                )

    def build(self) -> None:
        """
        Construye controladores lateralas del sidebar.
        1. Iterar metadata
        2. Boton 'Crerrar Sesion'
        3. Controladres 'Boton' - Ruta Vista
        4. Logo
        """
        self.PATHS = {}
        self.BUTTON = []

        MENU_KEYS = list(self.menu.keys())
        VIEW_KEYS = list(self.view.keys())

        if MENU_KEYS != VIEW_KEYS:
            raise KeyError

        for k in MENU_KEYS:

            menu_pack = self.menu.get(k)
            view_pack = self.view.get(k)

            label = menu_pack.get("label", "")
            route = menu_pack.get("route", "")
            emoji = menu_pack.get("icons", "").upper()

            path = view_pack.get("path", "")
            clas = view_pack.get("class", "")

            validate = (
                (label == ""),
                (route == ""),
                (emoji == ""),
                (path == ""),
                (clas == ""),
            )

            if any(validate):
                raise ValueError

            self.PATHS = {k: path}

            button = ft.TextButton(
                    content=label,
                    width=215,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.Colors.GREY_900},
                        color={"": ft.Colors.WHITE}
                    ),
                    icon=getattr(ft.Icons, emoji, None),
                    on_click=lambda e, r=path, c=clas: self.go_to(
                        e,
                        route=r,
                        view=c
                    )
                )

            self.BUTTON.append(button)

        # Agregar Estaticos en Sidebar
        self.BUTTON.insert(0, self.logout)
        self.BUTTON.append(ft.Text("ALAI INC.", weight=ft.FontWeight.W_400))
        self.controls = self.BUTTON

    def go_to(self, _, route, view) -> None:
        self.shell.view_extraction(route=route, view=view)

