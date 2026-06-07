# Modulos Python
from typing import List

# Modulos Terceros
import flet as ft

# Propios
from pancakes.models.model import PanCakesORM


class DatatableORM(ft.Column):
    """
    Atributos:

    model; El modelo renderizado, funciones, vistas, ... etc.
    controllers; Lista 'Peticion de componentes'.
    filters; Lista 'Peticion de filtros'.

    current_page; Ubicacion de Pagina.
    max_rows; Maximo de filas renderizadas por hoja.
    container; Query devuelto (Paquete de datos) vector = max_rows.
    table; Nombre de la tabla del modelo pasado.
    columns; Lista de tablas [strings, ... ].
    flet_columns; Columnas del query (listadas como objetos Flet).
    rows; Filas transpuestas crudas.
    flet_rows; Filas del query (listadas como objetos Flet).
    length; Largo del vector devuelto por el query actual.

    """

    def __init__(
        self, model: PanCakesORM, controllers: List = None, filters: List = None
    ):
        super().__init__()
        self.model = model
        self.controllers = controllers
        self.filters = filters

        self.current_page = 1
        self.max_rows = 15
        self.container = None
        self.table = None
        self.columns = []
        self.flet_columns = []
        self.rows = []
        self.flet_rows = []
        self.length = 0

        # Metodos
        self._calculate_chunk_()
        self._fetch_data_()
        self._construct_flet_columns_()
        self._construct_flet_rows_()
        self._vector_length_()
        self._page_counter_widget_()
        self._create_entry_widget_()
        self._table_widget_()
        self._sidebar_()
        self._layout_()

    # === Metodos inicializacion ===

    def _calculate_chunk_(self) -> None:
        """Tranforma indices 0,1,2 en rangos 20,40,60 etc..."""
        if self.current_page > 1:
            limit = self.max_rows * self.current_page
            offset = limit - self.max_rows
            self.chunk = {"offset": offset, "limit": limit}
        else:
            self.chunk = {"offset": 0, "limit": self.max_rows}

    def _fetch_data_(self) -> None:
        """Carga toda la tabla en memoria"""
        self.container = self.model.chunk(**self.chunk).all().container()

    def _construct_flet_columns_(self) -> None:
        """Extracción de columnas; Lista de columnas Flet"""
        self.table = self.model._table
        self.columns = []
        for column, metadata in self.container[self.table].items():
            validate = ((column != "@main_table@"), (column != "@depends@"))
            if all(validate):
                self.columns.append(column)

        self.flet_columns = [
            ft.DataColumn(
                label=ft.Text(str(self.container[self.table][COL]["label"]))
            )
            for COL in self.columns
        ]

    def _construct_flet_rows_(self) -> None:
        """Extraer y construir las filas del query devuelto actual"""
        raw = []  # Extraccion
        for field, metadata in self.container[self.table].items():
            validate = ((field != "@main_table@"), (field != "@depends@"))
            if all(validate):
                raw.append(metadata["vector"])

        # Filas crudas transpuestas
        self.rows = list(zip(*raw))

        # Filas FLet
        self.flet_rows = [
            ft.DataRow(
                on_select_change=None,  # Seleccion de fila
                selected=False,
                cells=[ft.DataCell(ft.Text(cell)) for cell in row],
            )
            for row in self.rows
        ]

    def _vector_length_(self) -> None:
        """Largo del query (vector)"""
        self.length = len(self.rows) if self.rows else 0

    def _page_counter_widget_(self) -> None:
        self.page_counter_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Button(content="-", on_click=self._counter_manager_),
                    ft.Text(self.current_page),
                    ft.Button(content="+", on_click=self._counter_manager_),
                ]
            )
        )

    def _create_entry_widget_(self) -> None:
        self.create_entry_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Button(
                        content="Nuevo",
                        on_click=lambda e: self.create_entry(e),
                        icon=ft.Icons.ADD
                    )
                ]
            )
        )

    def _table_widget_(self):
        datatable = ft.DataTable(
            columns=self.flet_columns,
            rows=self.flet_rows,
            show_checkbox_column=True,
        )
        self.datatable_container = ft.Container(
            content=ft.ListView(
                controls=[datatable], expand=True, horizontal=True
            ),
            bgcolor=ft.Colors.BLACK_12,
            border_radius=10,
            padding=5,
            expand=1,
        )

    # Contenedor Side Bar
    def _sidebar_(self):
        self.sidebar_container = ft.Container(
            content=None,
            bgcolor=ft.Colors.BLACK_12,
            border_radius=10,
            padding=5,
            expand=True,
            visible=False,
        )

    # === FUNCIONES Y LOGICA ===
    def _counter_manager_(self, e) -> None:
        """
        Query menor a max_rows, no renderiza mas cambios de pagina
        en el contador. Ademas que no puede renderizarse un contador menor a 1
        """
        pass

    def _validate_navigation_(self) -> None:
        if self.length > 0:
            self.current_page += 1

    def create_entry(self, e):
        self.sidebar_container.visible = not self.sidebar_container.visible
        self.form()
        self.sidebar_container.content = self.form_widget
        self.update()

    # === FORMULARIO ===
    def form(self):

        MODEL = self.model
        TABLE = self.table
        controls = []

        for COL in self.columns:

            field_name = self.container[TABLE][COL].get("label", "")
            field_pk = self.container[TABLE][COL].get("primary_key", False)
            field_type = self.container[TABLE][COL].get("sql_type", "").upper()
            field_position = self.container[TABLE][COL].get("position", "")
            field_read_only = self.container[TABLE][COL].get("readonly", False)
            field_required = self.container[TABLE][COL].get("required", False)
            sec_table = self.container[TABLE][COL].get("second_table", False)
            if sec_table:
                name = (
                    f"{sec_table}__{MODEL._metadata[sec_table]["columns"][1]}"
                )
            else:
                name = None
            required = "TRUE" if field_required else "FALSE"
            field_default = self.container[TABLE][COL].get("default", None)
            constraints = MODEL._metadata[TABLE]["schema"][COL]["constraints"]
            max_length = constraints.get("max_length", None)
            ge = constraints.get("ge", False)
            gt = constraints.get("gt", False)
            le = constraints.get("le", False)
            lt = constraints.get("lt", False)
            position = f"{TABLE}__{str(field_position)}__{required}"

            if field_pk:
                continue

            if field_type == "TEXT":
                component = ft.TextField(
                    label=field_name,
                    key=position,
                    read_only=field_read_only,
                    value=field_default
                )
                controls.append(ft.Row(controls=[component]))

            elif field_type == "VARCHAR":
                component = ft.TextField(
                    label=field_name,
                    key=position,
                    read_only=field_read_only,
                    max_length=max_length,
                    value=field_default
                )
                controls.append(ft.Row(controls=[component]))

            elif field_type == "INTEGER":
                component = ft.TextField(
                    label=field_name,
                    input_filter=ft.InputFilter(
                        allow=True,
                        regex_string=r"^[0-9]*$",
                        replacement_string=""
                    ),
                    keyboard_type=ft.KeyboardType.NUMBER,
                    key=position,
                    read_only=field_read_only,
                    value=field_default
                )
                controls.append(ft.Row(controls=[component]))

            elif field_type == "FLOAT":
                component = ft.TextField(
                    label=field_name,
                    input_filter=ft.InputFilter(
                        allow=True,
                        regex_string=r"^\d*\.?\d*$",
                        replacement_string=""
                    ),
                    keyboard_type=ft.KeyboardType.NUMBER,
                    key=position,
                    read_only=field_read_only,
                    value=field_default
                )
                controls.append(ft.Row(controls=[component]))

            elif field_type == "BOOL":
                VAL = field_default if field_default is not None else True
                component = ft.Switch(
                    label=field_name,
                    key=position,
                    read_only=field_read_only,
                    value=VAL
                )
                controls.append(ft.Row(controls=[component]))

            elif field_type == "DATE":

                if field_read_only:
                    component = ft.TextField(
                        label=field_name,
                        key=position,
                        read_only=field_read_only,
                        value=field_default
                    )

                else:
                    component = ft.DatePicker(
                        label=field_name,
                        key=position,
                        value=field_default
                    )

                controls.append(ft.Row(controls=[component]))

            elif field_type == "TIMESTAMP":

                if field_default is not None:
                    DATE = field_default.split("T")[0]
                    TIME = field_default.split("T")[1]
                else:
                    DATE = None
                    TIME = None

                if field_read_only:

                    component = ft.TextField(
                        label=field_name,
                        key=position,
                        read_only=field_read_only,
                        value=field_default
                    )

                else:
                    component = ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.DatePicker(
                                        label=field_name,
                                        key=position,
                                        read_only=field_read_only,
                                        value=DATE,
                                        width=200
                                    )
                                ],
                                expand=True
                            ),
                            ft.Column(
                                controls=[
                                    ft.TimePicker(
                                        label=field_name,
                                        key=position,
                                        read_only=field_read_only,
                                        value=TIME,
                                        width=200
                                    )
                                ],
                                expand=True
                            )
                        ],
                        expand=True
                    )

                controls.append(ft.Row(controls=[component]))

            elif field_type == "FOREIGN KEY":
                sub_model = MODEL._family[sec_table]
                ROW, COL = sub_model.select(name).all().raw(align=True)

                if ROW:
                    OPTIONS = list(ROW[0])
                else:
                    OPTIONS = ["vacio"]

                component = ft.Dropdown(
                    label=field_name,
                    key=position,
                    value = None,
                    options=[
                        ft.DropdownOption(key=str(op.upper()), text=str(op))
                        for op in OPTIONS
                    ]
                )

                controls.append(ft.Row(controls=[component]))

            else:
                raise TypeError(f"Unknown passed datatype {field_type}.")

        controls.append(
            ft.Button(
                content="Guardar Cambios",
                key="save",
                icon=ft.Icons.SAVE
            )
        )

        self.form_widget = ft.ListView(
                controls=[
                    ft.Column(
                        controls=controls,
                        spacing=20
                    )
                ],
            expand=True,
            horizontal=False
        )

    # === CAPA SUPERIOR; MONTAR WIDGETS ===
    def _layout_(self) -> None:
        header = ft.Row(
            controls=[self.page_counter_container, self.create_entry_container],
            expand=1,
        )
        content = ft.Row(
            controls=[self.datatable_container, self.sidebar_container],
            expand=11,
        )
        self.expand = True
        self.controls.extend([header, content])
