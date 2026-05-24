import flet as ft


class DataTableORM(ft.Column):
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
    Attr. instancia: active_row: Almacena la fila seleccionada.
    Attr. instancia: form_fields: Campos del formulario.

    Meth. instancia: unpack(); Separa: Posición, Columnas, Vectores
    Meth. instancia: make_columns(): De esta tabla; ft.Columns()
    Meth. instancia: init__datatable(): ft.DataTable() - ft.Container()
    Meth. instancia: mount_widgets(): Monta widgets en la fila ft.Row - (Padre).
    Meth. instancia: selected_row_manager(): Seleccion - Formulario
    Meth. instancia: selected_row(): Checkbox event
    Meth. instancia: edition_form(): Formulario de edicion
    """

    def __init__(self, container, width=None, backend_controller=None):
        super().__init__()

        self.container = container
        self.column_spacing = 15 if width is None else width
        self.backend_controller = backend_controller
        self.expand = True
        self.sheet_count = 0
        self.raw_data = {}
        self.display = []
        self.active_row = None
        self.unpack()
        self.make_columns()
        self.page_indexes()
        self.segment_data()
        self.make_rows()
        self.page_counter_widget_method()
        self.new_entry_button_method()
        self.init_page_counter()
        self.init_new_entry()
        self.init_datatable()
        self.init_sideform()
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
        """De esta tabla columnas"""
        columns = [
            ft.DataColumn(label=ft.Text(str(COL)))
            for COL in self.raw_data.keys()
        ]
        self.flet_columns = columns

    def page_indexes(self) -> None:
        """Numero Paginas: {indice: [indice, indice]}"""
        length = self.vector_length
        segments = {}
        spliter = 20
        chunks = (length // spliter) + 1
        counter = 0
        for i in range(chunks):
            segments.update({counter: [counter, counter + spliter]})
            counter += 1
        self.page_indexes_reference = segments

    def segment_data(self) -> None:
        """Hoja de 20 datos por indice de pagina"""
        sheet = []
        order = self.page_indexes_reference[self.sheet_count]
        for column, vector in self.raw_data.items():
            sheet.append(vector[order[0] : order[1]])
        self.display = sheet

    def make_rows(self) -> None:
        """Crear filas flet segmentadas, default primeras 20"""
        transposition = list(zip(*self.display))
        rows = [
            ft.DataRow(
                on_select_change=self.selected_row_manager,
                selected=False,
                cells=[ft.DataCell(ft.Text(cell)) for cell in row],
            )
            for row in transposition
        ]
        self.flet_rows = rows

    def page_counter_widget_method(self) -> None:
        self.current_page = ft.Text(value=0,weight=ft.FontWeight.BOLD)
        widget = ft.Row(
            controls=[
                ft.Column(
                    ft.FilledButton(
                        content="Volver",
                        icon=ft.Icons.REMOVE,
                        expand=1,
                        style=ft.ButtonStyle(shape=ft.StadiumBorder()),
                        key="previous_page",
                        on_click=self.sheet_manager
                    )
                ),
                ft.Column(
                    controls=self.current_page,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(
                    ft.FilledButton(
                        content="Avanzar",
                        icon=ft.Icons.ADD,
                        expand=1,
                        style=ft.ButtonStyle(shape=ft.StadiumBorder()),
                        key="next_page",
                        on_click=self.sheet_manager
                    )
                )
            ],
            expand=1,
            visible=True
        )
        self.page_counter_widget = widget

    def new_entry_button_method(self):
        widget = ft.Column(
            controls=[
                ft.FilledButton(
                    content="Nuevo Registro",
                    icon=ft.Icons.CREATE,
                    expand=True,
                    style=ft.ButtonStyle(shape=ft.StadiumBorder())
                )
            ],
            expand=1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.new_entry_widget = widget

    def init_page_counter(self) -> None:
        self.page_counter_container = ft.Container(
            expand=1,
            content=self.page_counter_widget,
            bgcolor=ft.Colors.BLACK_12,
            border_radius=10,
            padding=15
        )

    def init_filters(self) -> None:
        pass

    def init_new_entry(self):
        self.new_entry_container = ft.Container(
            expand=1,
            content=self.new_entry_widget,
            bgcolor=ft.Colors.BLACK_12,
            border_radius=10,
            padding=15
        )

    def init_datatable(self) -> None:
        self.datatable = ft.DataTable(
            columns=self.flet_columns,
            rows=self.flet_rows,
            show_checkbox_column=True,
        )
        self.datatable_container = ft.Container(
            expand=2,
            content=ft.ListView(controls=[self.datatable], expand=True),
            bgcolor=ft.Colors.BLACK_12,
            border_radius=10,
            padding=5,
        )

    def init_sideform(self):
        self.sideform_container = ft.Container(
            expand=2,
            content=None,
            bgcolor=ft.Colors.BLACK_12,
            border_radius=10,
            padding=5,
            visible=False
        )

    def mount_widgets(self) -> None:
        headers_row = ft.Row(
            controls=[
                self.page_counter_container,
                self.new_entry_container
            ],
            expand=1
        )
        content_row = ft.Row(
            controls=[
                self.datatable_container,
                self.sideform_container
                ],
            expand=10
        )
        self.controls.extend(
            [
            headers_row,
            content_row
            ]
        )

    def selected_row_manager(self, e) -> None:
        # Control del evento de seleccion guardado
        if e != self.active_row and self.active_row is not None:
            self.active_row.selected = not self.active_row.selected
        self.active_row = e.control
        self.fill_form()
        self.selected_row(e)

    def fill_form(self):
        columns = list(self.raw_data.keys())
        fields = []

        for idx, cell in enumerate(self.active_row.cells):
            fields.append(
                ft.TextField(
                    label=columns[idx],
                    value=cell.content.value
                )
            )
        fields.append(ft.FilledButton(content="Guardar"))
        form = ft.ListView(controls=fields, expand=True, spacing=25)
        self.form = form

    def selected_row(self, e) -> None:
        """ Toggle de checkbox de fila """
        e.control.selected = not e.control.selected
        self.sideform_container.visible = not self.sideform_container.visible
        self.sideform_container.content = self.form
        self.update()

    def page_counter_on_change(self, llave):
        index = int(self.current_page.value)
        if llave == "previous_page" and index > 0:
            self.current_page.value -= 1
        if llave == "next_page" and index < list(self.page_indexes_reference.keys())[-1]:
            self.current_page.value += 1

    def sheet_manager(self, e):
        llave = e.control.key
        if llave in ("previous_page", "next_page"):
            self.page_counter_on_change(llave)
        self.page.update()
