import flet as ft

from ..backend.expose_models import get_inv_dicc, get_inv_json, get_inv_raw


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

        table = ft.Row(controls=[
        ft.Text(get_inv_raw()),
        ft.Text(get_inv_dicc()),
        ft.Text(get_inv_json())
        ])

        root = ft.Column(
            controls=[
                topbar,
                table
            ]
        )

        return root
