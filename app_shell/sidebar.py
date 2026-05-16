import flet as ft


class Sidebar(ft.Column):
    """
    Construccion de sidebar;
    Se inyecta la metadata de los paquetes (__manifest__)
    Construccion dinamica de botones y rutas de navegacion.
    """

    def __init__(
        self,
        metadata,
        shell,
        app_page: ft.Page
    ):
        super().__init__()
        # Variables de construccion
        self.metadata = metadata
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
        3. Controladres 'Boton'
        4. Logo
        """

        self.ROUTES = {}
        self.BUTTON = []
        # Iteracion anidada de; {pack, {labe: data}, ...}
        for pack, meta in self.metadata.items():
            # Lista de botones metadata
            MENU = meta.get("menus", [])
            # Validar lista
            if not MENU:
                raise ValueError(
                    f"Invalid metadata for following package: '{pack}'. "
                    "KEY; 'menu' was not found or its empty."
                )
            # Iteracion de boton | ruta
            for controller in MENU:
                label = controller.get("label", "")
                route = controller.get("route", "")
                emoji = controller.get("icons", "").upper()

                if (label == "" or route == "" or emoji == ""):
                    raise ValueError(
                        "Either 'label' or 'route' keys were empty. "
                        "Another posibility: They were not found in "
                        "'menus' keys."
                        f"menus - {MENU}, label - {label}, route - {route} "
                        f"icons - {emoji}."
                    )

                self.ROUTES.update({label: route})

                button = ft.TextButton(
                    content=label,
                    width=215,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.Colors.GREY_900},
                        color={"": ft.Colors.WHITE}
                    ),
                    icon=getattr(ft.Icons, emoji, None),
                    on_click=lambda e, r=route: self.go_to(
                        e,
                        r
                    )
                )

                self.BUTTON.append(button)

        # Agregar Estaticos en Sidebar
        self.BUTTON.insert(0, self.logout)
        self.BUTTON.append(ft.Text("ALAI INC.", weight=ft.FontWeight.W_400))
        self.controls = self.BUTTON

    def go_to(self, _, route) -> None:
        composed_route = f"packages.{route}"
        self.shell.navigate(self.shell, route=composed_route)
