import flet as ft


class DataTableORM(ft.DataTable):
    def __init__(self, headers, lines):
        super().__init__()
        self.headers = headers
        self.lines = lines
        self._tranform_arguments_()

    def _tranform_arguments_(self) -> None:
        columns = [ft.DataColumn(label=ft.Text(c)) for c in self.headers]
        rows = [ft.DataRow(cells=[cell for cell in R]) for R in self.lines]

        self.columns = columns
        self.rows = rows

        return