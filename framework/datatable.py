import flet as ft


class DataTableORM(ft.Row):

    def __init__(self, container, width=None):
        super().__init__()

        self.container = container
        self.column_spacing = 15 if width is None else width
        self.expand = False

        self.unpack()

    def selection(self, e):
        return

    def unpack(self):

        self.content = self.container[0]
        self.positions = self.content["@positions@"]

        TABLES = []

        for tags, values in self.content.items():
            if tags != "@positions@":
                TABLES.append(tags)

        DATATABLE = {}
        VECTORS = []

        for TAB in TABLES:
            DICC = self.content[TAB]

            for column, values in DICC.items():
                DATATABLE.update({column: values})
                VECTORS.append(values)

        TRANS = list(zip(*VECTORS))

        columns = [
            ft.DataColumn(label=ft.Text(str(COL)))
            for COL in DATATABLE.keys()
        ]

        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cell)))
                    for cell in row
                ],
                on_select_change=self.selection,
            )
            for row in TRANS
        ]

        self.datatable = ft.DataTable(
            columns=columns,
            rows=rows,
            show_checkbox_column=True,
        )

        self.controls.append(
            ft.Container(
                expand=True,
                content=self.datatable,
                bgcolor=ft.Colors.BLUE_GREY_100,
                border_radius=10,
                padding=10,
            )
        )