import flet as ft


class View(ft.Stack):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.Column(
            controls=[ft.Text("Inv."), ft.Text("Prueba funcional")]
        )
