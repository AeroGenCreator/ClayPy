import flet as ft


class EjePrincipal(ft.Row):
    def __init__(self, modulos, pagina):
        super().__init__()
        self.modulos = modulos
        self.pagina = pagina
        # sidebar contenedor
        self.sidebar = ft.Container(content=None)
        # contenido_vista_contendor
        self.contenido_vista = ft.Container(content=None)
        self.contruir_botones()

    def manejar_click(self, e):
        boton = e.control
        modulo = boton.key
        metadata = getattr(self, modulo, None)
        if metadata is None:
            ValueError("Unreachable metadata view.")
        first_key = list(metadata.keys())[0]
        function = metadata[first_key]
        view = function()
        self.contenido_vista = ft.Container(
            content=ft.Column(controls=view),
            expand=11
        )
        self.controls = [self.sidebar, self.contenido_vista]
        self.pagina.update()

    def contruir_botones(self):

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
            content=ft.Column(controls=sidebar_botones),
            padding=10,
            border_radius=10,
            expand=1
        )
        self.controls = [self.sidebar, self.contenido_vista]
        self.pagina.update()


class ContenidoVista(ft.Column):
    def __init__(self, modelo, navegacion):
        super().__init__()
        self.modelo = modelo
        self.navegacion = navegacion
    pass
