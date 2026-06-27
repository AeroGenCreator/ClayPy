# Lanzador de aplicacion

# Carga de metadata
import flet as ft

from claypy.container import MainContainer, ShellContaniner
from claypy.package_loader import load_models, mapper, read_manifest

# 1. Correccion; Lectura del manifest
container_items, sidebar_button, dynamic_models = read_manifest()
# 2. Carga de todos los modelos declarados en el maniest
load_models(dynamic_models)
# 3. Mapea "Boton" | "evento"
controllers = mapper(content=container_items, sidebar_button=sidebar_button)
# PENDIENTE: SHELL, CONTAINER, SIDEBAR(event handler)


"""
#from app_shell.container import MainContainer
#from app_shell.shell import ClayPyShell
#from app_shell.sidebar import Sidebar
from framework.package_loader import package_loader, run_models

# Lectura de los manifest
loaded_menu, loaded_view, loaded_models = package_loader()
# Ejecución de los modelos.
run_models(models_pack=loaded_models)


    container = MainContainer(content=None)
    sidebar = Sidebar(
        menu=loaded_menu,
        view=loaded_view,
        app_page=page,
        shell=ClayPyShell(container=container, page=page)
    )

    page.add(
        ft.Row(
            controls=[sidebar, container],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH
        )
    )
"""


def main(page: ft.Page):
    page.title = "ClayPy"
    page.window.width = 1920
    page.window.height = 1080

    # Este contenedor debe ser de login.
    main_container = MainContainer(
        contenido=ft.Column(
            controls=[
                ft.Text("Hola")
            ]
        ),
        pagina=page
    )

    # Este contenedor renderiza la aplicación.
    shell_container = ShellContaniner(
        contenido=None,
        pagina=page
    )

    page.add(
        main_container,
        shell_container
    )


if __name__ == "__main__":
    ft.run(main)
