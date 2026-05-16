# Lanzador de aplicacion

# Carga de metadata
import flet as ft
from app_shell.container import MainContainer
from app_shell.sidebar import Sidebar
from app_shell.shell import Shell
from framework.package_loader import package_loader

loaded_metadata = package_loader()

def main(page: ft.Page):
    sidebar = Sidebar(
        metadata=loaded_metadata,
        app_page=page,
        shell=Shell
    )
    container = MainContainer(content=ft.Text("CONT"))
    black_box = Shell(page=page, sidebar=sidebar, container=container)

if __name__ == "__main__":
    ft.run(main)
