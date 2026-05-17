# Lanzador de aplicacion

# Carga de metadata
import flet as ft

from app_shell.container import MainContainer
from app_shell.shell import ClayPyShell
from app_shell.sidebar import Sidebar
from framework.package_loader import package_loader

loaded_metadata = package_loader()

def main(page: ft.Page):

    container = MainContainer(content=None)
    sidebar = Sidebar(
        metadata=loaded_metadata,
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
