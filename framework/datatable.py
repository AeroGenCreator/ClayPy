import flet as ft


class DataTableORM(ft.Row):
    """
    Attr. instancia: container; Toda la data ORM
    Attr. instancia: content: ORM diccionario
    Attr. instancia: positions: {tabla: {columnas: posicion}}
    Attr. instancia: vector_length: Total de filas
    Attr. instancia: column_spacing; Espacio entre columnas
    Attr. instancia: expand: Usar toda la fila
    Attr. instancia: sheet_count: Indice de pagina actual
    Attr. instancia: raw_data: {columna: vector}
    Attr. instancia: display: Vector indexado segun condicion (pagina | filtro)
    Attr. instancia: flet_columns: De esta tabla List[ft.Columns]
    Attr. instancia: flet_rows: De esta tabla List[ft.RowData()]
    Attr. instancia: datatable: ft.DataTable() - objeto
    Attr. instancia: datatable_container: ft.Container(ft.DataTable())

    Meth. instancia: unpack(); Separa: Posición, Columnas, Vectores
    Meth. instancia: make_columns(): De esta tabla; ft.Columns()
    Meth. instancia: init__datatable(): ft.DataTable() - ft.Container()
    Meth. instancia: mount_widgets(): Monta widgets en la fila ft.Row - (Padre).
    Meth. instancia: selected_row_manager(): Seleccion - Formulario
    Meth. instancia: selected_row(): Checkbox event
    Meth. instancia: edition_form(): Formulario de edicion
    """

    def __init__(self, container, width=None):
        super().__init__()

        self.container = container
        self.column_spacing = 15 if width is None else width
        self.expand = False
        self.sheet_count = 0
        self.raw_data = {}
        self.display = []
        self.edition_form = ft.NavigationDrawer()
        self.unpack()
        self.make_columns()
        self.page_indexes()
        self.segment_data()
        self.make_rows()
        self.init__datatable()
        self.mount_widgets()

    def transposition_data_filter(self, index):
        pass

    def transposition_data(self, index):
        pass

    def registration_form(self, e):
        pass

    def unpack(self):
        """Preparar datos desde container ORM para renderizar"""
        self.content = self.container[0]  # Paquete
        self.positions = self.content["@positions@"]  # Posiciones

        TABLES = []

        for tags, values in self.content.items():
            if tags != "@positions@":
                TABLES.append(tags)

        self.raw_data = {}
        VECTORS = []

        for TAB in TABLES:
            DICC = self.content[TAB]

            for column, values in DICC.items():
                self.raw_data.update({column: values})
                VECTORS.append(values)

        self.vector_length = len(VECTORS[0])

    def make_columns(self):
        """ De esta tabla columnas """
        columns = [
            ft.DataColumn(
                label=ft.Text(str(COL))
            )
            for COL in self.raw_data.keys()
        ]
        self.flet_columns = columns

    def page_indexes(self) -> None:
        """ Numero Paginas: {indice: [indice, indice]}"""
        length = self.vector_length
        segments = {}
        spliter = 20
        chunks = (length // spliter) + 1
        counter = 0
        for i in range(chunks):
            segments.update({counter: [counter, counter + spliter]})
            counter += spliter
        self.page_indexes_reference = segments

    def segment_data(self) -> None:
        """ Hoja de 20 datos por indice de pagina """
        sheet = []
        order = self.page_indexes_reference[self.sheet_count]
        for column, vector in self.raw_data.items():
            sheet.append(
                vector[order[0]: order[1]]
            )
        self.display = sheet

    def make_rows(self) -> None:
        """ Crear filas flet segmentadas, default primeras 20 """
        transposition = list(zip(*self.display))
        rows = [
            ft.DataRow(
                on_select_change=self.selected_row_manager,
                selected=False,
                cells=[
                    ft.DataCell(
                        ft.Text(cell)
                )
                for cell in row]
            )
            for row in transposition
        ]
        self.flet_rows = rows

    def init__datatable(self) -> None:
        self.datatable = ft.DataTable(
            columns=self.flet_columns,
            rows=self.flet_rows,
            show_checkbox_column=True
        )
        self.datatable_container = ft.Container(
            expand=True,
            content=self.datatable,
            bgcolor=ft.Colors.BLUE_GREY_100,
            border_radius=10,
            padding=0
        )

    def mount_widgets(self) -> None:
        self.controls.append(self.datatable_container)

    def selected_row_manager(self, e) -> None:
        self.selected_row(e)
        self.sidebar_drawer(e)
        pass

    def selected_row(self, e) -> None:
        check = e.control.selected
        if check:
            e.control.selected = False
        else:
            e.control.selected = True
        self.update()

    async def sidebar_drawer(self, e) -> None:
        edition_form(e=e)
        await self.datatable_container.show_drawer()

    def edition_form(self, e):
        drawer = ft.NavigationDrawer(
            controls=[ft.Text("Abierto")]
        )
        pass

    def sheet_manager(self, e):
        # Si cambio de pagina
        # Si filtro
        pass

