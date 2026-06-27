import flet as ft


class EjePrincipal(ft.Row):
    def __init__(self, modulos, pagina):
        super().__init__()
        self.modulos = modulos
        self.pagina = pagina
        # sidebar contenedor
        self.sidebar = ft.Container(content=None)
        # navegador
        self.navegador = ft.Container(content=None)
        # contenido_vista_contendor
        self.contenido_vista = ft.Container(content=None)
        self.construir_botones_sidebar()

    def navegar_modulo(self):
        pass

    def construir_navegacion(self, modulo):
        metadata = getattr(self, modulo, None)
        if metadata is None:
            raise ValueError("Error when building navigation bar.")

        nav_buttons = []
        for label, function in metadata.items():
            nav_buttons.append(
                ft.Button(
                    content=label,
                    on_click=self.navegar_modulo
                )
            )

        self.navegador = ft.Container(
            content=ft.ListView(
                ft.Row(
                    controls=nav_buttons
                )
            ),
            expand=1
        )

    def manejar_click(self, e):
        boton = e.control
        modulo = boton.key
        metadata = getattr(self, modulo, None)
        if metadata is None:
            ValueError("Unreachable metadata view.")
        first_key = list(metadata.keys())[0]
        function = metadata[first_key]
        view = function()
        self.construir_navegacion(modulo=modulo)
        self.tabla = ft.Container(
            content=ft.Row(
                controls=view
            ),
            expand=11
        )
        self.contenido_vista = ft.Container(
            content=ft.Column(
                controls=[self.navegador, self.tabla]
            ),
            expand=10
        )
        self.controls = [self.sidebar, self.contenido_vista]
        self.pagina.update()

    def construir_botones_sidebar(self):

        sidebar_botones = []
        for element in self.modulos:
            for modulo, metadata in element.items():
                sidebar = metadata.get("sidebar", None)
                navigation = metadata.get("navigation", None)

                if sidebar is None or navigation is None:
                    raise ValueError("Empty metadata in modules. Stop Process")

                function = sidebar.get("function", None)
                label = sidebar.get("label", None)
                icon = sidebar.get("icon", None)

                # No valido el icono porque este puede ser None.
                validate = ((function is None),(label is None))

                if any(validate):
                    raise ValueError("Sidebar empty metadata error.")

                button = ft.Button(
                    icon=getattr(ft.Icons, icon, None),
                    on_click=self.manejar_click,
                    content=label,
                    key=modulo,
                )

                sidebar_botones.append(button)

                # La instancia ahora almacena:
                # Modulo como atributo, metadata de navegacion como contenido.
                setattr(self, modulo, navigation)

        # Aqui se maneja la arquitectura de montado
        self.sidebar = ft.Container(
            content=ft.ListView(
                controls=ft.Column(
                    controls=sidebar_botones
                )
            ),
            padding=10,
            border_radius=10,
            expand=2
        )
        self.controls = [self.sidebar, self.contenido_vista]
        self.pagina.update()


class ContenidoVista(ft.Column):
    def __init__(self, modelo, navegacion):
        super().__init__()
        self.modelo = modelo
        self.navegacion = navegacion
    pass
