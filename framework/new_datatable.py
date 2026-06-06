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
        self._table_widget_()
        self._layout_()

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
            ft.DataColumn(label=ft.Text(str(COL))) for COL in self.columns
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
                    ft.Button(
                        content="-",
                        on_click=self._counter_manager_
                    ),
                    ft.Text(self.current_page),
                    ft.Button(
                        content="+",
                        on_click=self._counter_manager_
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
                controls=[datatable],
                expand=True,
                horizontal=True
            ),
            bgcolor=ft.Colors.BLACK_12,
            border_radius=10,
            padding=5,
        )

    def _counter_manager_(self, e) -> None:
        """
        Query menor a max_rows, no renderiza mas cambios de pagina
        en el contador. Ademas que no puede renderizarse un contador menor a 1
        """
        pass

    def _validate_navigation_(self) -> None:
        if self.length > 0:
            self.current_page += 1

    def _layout_(self) -> None:
        headers_row = ft.Row(
            controls=[self.page_counter_container],
            expand=1,
        )
        content_row = ft.Row(
            controls=[self.datatable_container],
            expand=11,
        )
        self.expand = True
        self.controls.extend([headers_row, content_row])
