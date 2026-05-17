import flet as ft
from ..backend.expose_models import get_inventory

class View(ft.Column):
    def __init__(self):
        super().__init__()

    def build(self):

        topbar = ft.Row(
            controls=[
                ft.TextButton("Inventario"),
                ft.TextButton("Ingredientes"),
                ft.TextButton("Categorias")
            ]
        )

        table = ft.Text(get_inventory()) 

        root = ft.Column(
            controls=[
                topbar,
                table
            ]
        )
        
        return root
