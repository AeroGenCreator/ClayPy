# Lanzador de aplicacion

# Carga de metadata
import flet as ft

from app_shell.container import MainContainer
from app_shell.sidebar import Sidebar
from framework.package_loader import package_loader

loaded_metadata = package_loader()

def main(page: ft.Page):
    bar = Sidebar(
        metadata=loaded_metadata,
        app_page=page
    )
    con = MainContainer(content=ft.Text("CONT"))

    page.add(
        ft.Row(
            controls=[
            bar,
            ft.VerticalDivider(),
            con
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH
        )
    )

if __name__ == "__main__":
    ft.run(main)
