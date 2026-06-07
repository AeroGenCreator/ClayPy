# Lanzador de aplicacion

# Carga de metadata
import flet as ft

from app_shell.container import MainContainer
from app_shell.shell import ClayPyShell
from app_shell.sidebar import Sidebar
from framework.package_loader import package_loader, run_models

loaded_menu, loaded_view, loaded_models = package_loader()
run_models(models_pack=loaded_models)

def main(page: ft.Page):
    page.title = "ClayPy Framework"
    page.window.width = 1920
    page.window.height = 1080

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

if __name__ == "__main__":
    ft.run(main)
