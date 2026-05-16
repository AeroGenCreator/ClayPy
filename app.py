# Lanzador de aplicacion

# Carga de metadata
import flet as ft

from app_shell.sidebar import Sidebar
from framework.package_loader import package_loader

loaded_metadata = package_loader()

def main(page: ft.Page):

    page.add(
        ft.Row(
            controls=[
            Sidebar(
                metadata=loaded_metadata,
                app_page=page
            )]
        ),
        ft.Row(
            controls=[ft.Text("ALAI INC.", weight=ft.FontWeight.W_400)],
            vertical_alignment=ft.CrossAxisAlignment.END
        )
    )

if __name__ == "__main__":
    ft.run(main)
