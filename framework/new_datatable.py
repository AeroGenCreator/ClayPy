# Modulos Python
from typing import List

# Modulos Terceros
import flet as ft

# Propios
from pancakes.models.model import PanCakesORM


class DatatableORM:
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
    flet_columns; Columnas de este modelo (Inicializadas como objetos Flet).

    """

    def __init__(
        self, model: PanCakesORM, controllers: List = None, filters: List = None
    ):
        self.model = model
        self.controllers = controllers
        self.filters = filters

        self.current_page = 1
        self.max_rows = 15
        self.container = None
        self.table = None
        self.columns = []
        self.flet_columns = []

        # Metodos
        self._calculate_chunk_()
        self._fetch_data_()
        self._construct_flet_columns_()
        self._calculate_page_counter_posibilities_()

    def _calculate_chunk_(self) -> None:
        """Tranforma indices 0,1,2 en rangos 20,40,60 etc..."""
        if self.current_page > 1:
            limit = self.max_rows * self.current_page
            offset = limit - self.max_rows
            self.chunk = {"offset": offset, "limit": limit}
        else:
            self.chunk = {"offset": 0, limit: self.max_rows}

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

    def _calculate_page_counter_posibilities_(self):
        """
        Query menor a max_rows, no renderiza mas cambios de pagina
        en el contador. Ademas que no puede renderizarse un contador menor a 1
        """
        pass
