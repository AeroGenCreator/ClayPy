import flet as ft


class DataTableORM(ft.Row):
    """
    Attr. instancia: container
    Attr. instancia: content
    Attr. instancia: positions
    Attr. instancia: columns
    Attr. instancia: tables
    Attr. instancia: datatable   

    """
    def __init__(self, container):
        super().__init__()
        self.container = container
        self.unpack()

    def unpack(self) -> None:
        self.content = self.container[0]  #  Indexar el contenido
        self.positions = self.content["@positions@"]
        
        TABLES = []  # Tablas del componente
        for tags, values in self.content.items():
            if tags != "@positions@":
                TABLES.append(tags)
        
        self.columns = []  # Columnas sin formato
        self.tables = []  # Tablas alineadas con columnas NO FORMATO
        DATATABLE = {}  # Columnas con formato: valores
        VECTORS = []
        for TAB in TABLES:
            DICC = self.content[TAB]
            for column, values in DICC.items():
                DATATABLE.update({f"{TAB} {column}": values})
                VECTORS.append(values)
                self.columns.append(column)
                self.tables.append(TAB)

        TRANS = list(zip(*VECTORS)) 
        COLUMNS = [ft.DataColumn(label=ft.Text(COL)) for COL in DATATABLE.keys()]
        ROWS = [ft.DataRow(cells=[ft.DataCell(ft.Text(cell)) for cell in row]) for row in TRANS]

        datatable = ft.DataTable(
            columns=COLUMNS,
            rows=ROWS,
        )

        self.datatable = datatable

    def build(self) -> None:
        self.controls = [self.datatable]

        return