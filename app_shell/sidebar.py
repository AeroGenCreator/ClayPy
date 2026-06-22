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

        # Declaracion de rutas y botones para el sidebar.
        self.PATHS = {}
        self.BUTTON = []

        # Valida que existan las mismas llaves en la petición de menu y vista.
        MENU_KEYS = list(self.menu.keys())
        VIEW_KEYS = list(self.view.keys())

        if MENU_KEYS != VIEW_KEYS:
            raise KeyError(
                "Module name mismath when creating sidebar. "
                f"{MENU_KEYS} : {VIEW_KEYS} missmatch."
            )

        # Iteración de llaves.
        # Se puede acceder a ambos diccionarios;
        # gracias a las llaves compartidas.
        for modulo in MENU_KEYS:

            # Diccionarios de datos por moduloo (menu | vista)
            menu_pack = self.menu.get(modulo)
            view_pack = self.view.get(modulo)

            # Configuración del boton de app.
            label = menu_pack.get("label", "")
            route = menu_pack.get("route", "")
            icons = menu_pack.get("icons", "").upper()

            # Ruta a la vista del modulo cargado.
            path = view_pack.get("path", "")
            clas = view_pack.get("class", "")

            validate = (
                (label == ""),
                (route == ""),
                (icons == ""),
                (path == ""),
                (clas == ""),
            )

            if any(validate):
                raise ValueError(
                    "Informacion clave faltante en la declaración de mainifest."
                )

            # Se almacena "modulo" | "ruta a vista."
            self.PATHS = {modulo: path}

            # Creacion de boton principal de app.
            # Carga de función de redirección: self.go_to()
            # Recibe la ruta a la vista principal.
            button = ft.TextButton(
                    content=label,
                    width=215,
                    style=ft.ButtonStyle(
                        bgcolor={"": ft.Colors.GREY_900},
                        color={"": ft.Colors.WHITE}
                    ),
                    icon=getattr(ft.Icons, icons, None),
                    on_click=lambda e, r=path, c=clas: self.go_to(
                        e,
                        route=r,
                        view=c
                    )
                )

            self.BUTTON.append(button)

        # Agregar Estaticos en Sidebar
        self.BUTTON.insert(0, self.logout)
        self.BUTTON.append(ft.Text("BETA 1.0", weight=ft.FontWeight.W_400))
        self.controls = self.BUTTON

    def go_to(self, _, route, view) -> None:
        """
        El obbjeto "shell" cuenta con una función:
        'view_extraction': La cual monta la vista 'main' del modulo
        gracias a la ruta que dispara el boton construido en 'sidebar'.
        """
        self.shell.view_extraction(route=route, view=view)

