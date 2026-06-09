# Modulos Python
from typing import List
import uuid

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
    counter;
    form_controls;
    alert;

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
        self.counter = 1
        # Almacena los campos widgets de vista formulario 'invocada'
        self.form_controls = []
        self.alert = ft.AlertDialog()
        self.date_picker = ft.DatePicker()
        self.time_picker = ft.TimePicker()

        # Metodos
        self._calculate_chunk_()
        self._fetch_data_()
        self._construct_flet_columns_()
        self._construct_flet_rows_()
        self._vector_length_()
        self._page_counter_widget_()
        self._create_entry_widget_()
        self._table_widget_()
        self._table_container_()
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
                on_select_change=lambda e: self.current_row,  # Seleccion fila.
                selected=False,
                cells=[ft.DataCell(ft.Text(cell)) for cell in row],
            )
            for row in self.rows
        ]

    def _vector_length_(self) -> None:
        """Largo del query actual (vector)"""
        self.length = len(self.rows) if self.rows else 0

    def _page_counter_widget_(self) -> None:
        """Contiene el contador de paagina"""

        # Contador Numerico
        self.counter = ft.Text(value=self.current_page)
        # Conjunto de componentes (boton, numero, boton)
        self.page_counter_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Button(content="-", on_click=self._counter_manager_),
                    self.counter,
                    ft.Button(content="+", on_click=self._counter_manager_),
                ]
            )
        )

    def _create_entry_widget_(self) -> None:
        """Boton de nuevo registro, genera instancia de formulario vacio"""
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
        """Instancia 'Datatable, permite alterar filas.'"""
        self.datatable = ft.DataTable(
            columns=self.flet_columns,
            rows=self.flet_rows,
            show_checkbox_column=True,
        )

    def _table_container_(self):
        """Se monta el componente 'Datatable' en un contenedor"""
        self.datatable_container = ft.Container(
            content=ft.ListView(
                controls=[self.datatable], expand=True, horizontal=True
            ),  # Permite 'scroll' horizontal
            bgcolor=ft.Colors.BLACK_12,
            border_radius=10,
            padding=5,
            expand=1,
        )

    # Contenedor Side Bar
    def _sidebar_(self):
        """Contendor dinamico, vista formulario se monta en este contenedor"""
        self.sidebar_container = ft.Container(
            content=None,
            bgcolor=ft.Colors.BLACK_12,
            border_radius=10,
            padding=5,
            expand=True,
            visible=False,  # Este campo controla si se muestra o no.
        )

    # === FUNCIONES Y LOGICA ===

    def _counter_manager_(self, e) -> None:
        """
        Evalua el tipo de evento (avanzar, retroceder)
        Crea copias de 'current_page' & 'container'
        Se altera el contador, se realizar el query.
        Si la cuenta y el query son validos; los muestra
        De lo contrario regresa al estado original usando los respaldos.
        """
        if e.control.content == "-":
            if self.current_page > 1:
                self.current_page -= 1
                self._calculate_chunk_()
                self._fetch_data_()
                self._construct_flet_rows_()
                self.datatable.rows = self.flet_rows
                self.counter.value = self.current_page
                self.update()
        if e.control.content == "+":
            self.current_page_cache = self.current_page
            self.container_cache = self.container
            self.current_page += 1
            self._calculate_chunk_()
            self._fetch_data_()
            self._construct_flet_rows_()
            self._vector_length_()
            if self.length > 1:
                self.datatable.rows = self.flet_rows
                self.counter.value = self.current_page
                self.update()
            else:
                self.current_page = self.current_page_cache
                self.container = self.container_cache
                self._construct_flet_rows_()
                self.datatable.rows = self.flet_rows
                self.counter.value = self.current_page
                self.update()

    def create_entry(self, e):
        """
        Si se presiona:
        'Nuevo' -> Genera Formulario Limpio del Modelo -> Abre Vista
        Si se presiona Segunda Vez:
        -> Se borra el formulario -> Cierra Vista
        """
        status = self.sidebar_container.visible
        if status:
            self.sidebar_container.visible = not self.sidebar_container.visible
            self.sidebar_container.content = None
        else:
            self.sidebar_container.visible = not self.sidebar_container.visible
            self.form()
            self.sidebar_container.content = self.form_widget
        self.update()

    def current_row(self) -> None:
        pass

    def save_changes(self, e) -> None:

        data = []

        # Iterar controladores del formulario
        for field in self.form_controls:
            if isinstance(
                field,
                (ft.TextField, ft.Switch)
            ):
                name = field.label
            else:
                name = field.content
            # key almacena metada [datetime][tabla, posicion & validacion]:
            PARTS = field.key.split("__")

            # En caso de ser un widget dividido (TIMESTAMP)
            nature = None
            if len(PARTS) == 6:
                nature = PARTS[0]
                table = PARTS[1]
                column = PARTS[2]
                position = int(PARTS[3])
                required = PARTS[4]
                code = PARTS[5]
            # Resto de situaciones
            else:
                table = PARTS[0]
                column = PARTS[1]
                position = int(PARTS[2])
                required = PARTS[3]
                code = PARTS[4]

            if not isinstance(field, ft.Button):
                value = field.value
            else:
                value = field.content
            if required == "TRUE" and not value:
                self.required_alert(campos=name)
                return

            data.insert(position, value)
        kwargs = {self.model._table: [tuple(data)]}
        self.model.i(**kwargs)

    def required_alert(self, campos: list | str = "Aun No Hay Campos") -> None:
        """
        Esta funcion construye la alerta de campo requerido en tiempo real.
        """
        self.alert.title = "Restriccion"
        self.alert.content = ft.Text(
            value=f"Los siguientes campos son requeridos: {campos}"
        )
        self.alert.actions=[
            ft.TextButton(
                "Cerrar",
                on_click=lambda e: self.page.pop_dialog()
                )
            ]
        self.alert.open = True
        self.page.show_dialog(self.alert)
    
    # === FORMULARIO ===

    def form(self) -> None:
        """Creacion de formulario 'Nuevo' o 'Registro'"""

        # Constantes
        MODEL = self.model
        TABLE = self.table
        TITLE = ft.Container(
            content=ft.Text(
                value="Vista Formulario",
                weight=ft.FontWeight.W_900
            )
        )

        # Titulo 'Vista Formulario'
        controls = [TITLE]

        # Limpia widget formularios antiguos
        self.form_controls = []

        # Iteracion de 'nombre columnas' crudas
        for COL in self.columns:

            # Extraccion de metadata y restricciones
            field_type = self.container[TABLE][COL].get("sql_type", "").upper()
            field_read_only = self.container[TABLE][COL].get("readonly", False)
            field_required = self.container[TABLE][COL].get("required", False)
            sec_table = self.container[TABLE][COL].get("second_table", False)
            field_pk = self.container[TABLE][COL].get("primary_key", False)
            field_position = self.container[TABLE][COL].get("position", "")
            field_name = self.container[TABLE][COL].get("label", "")

            # Si existe N:1 -> Definimos un nombre de columna para el query
            if sec_table:
                name = (
                    f"{sec_table}__{MODEL._metadata[sec_table]["columns"][1]}"
                )
            else:
                name = None

            # Required puede ser usado para validar. Aunque pydantic ya lo hace.
            required = "TRUE" if field_required else "FALSE"


            field_default = self.container[TABLE][COL].get("default", None)

            # Extraccion de restricciones unicas de campo
            constraints = MODEL._metadata[TABLE]["schema"][COL]["constraints"]
            max_length = constraints.get("max_length", None)
            ge = constraints.get("ge", False)
            gt = constraints.get("gt", False)
            le = constraints.get("le", False)
            lt = constraints.get("lt", False)

            # Position es una llave unica que almacena metadata 'procesamiento'.
            position = (
                f"{TABLE}__"  # Nombre de Tabla
                f"{COL}__"  # Columna "crudo"
                f"{str(field_position)}__"  # Posicion en la tabla
                f"{required}__"  # Si es campo requerido
                f"{str(uuid.uuid4())}"  # Codigo unico
            )

            # Si el campo es un PrimaryKey NO renderizamos en formulario.
            if field_pk:
                continue

            # Se renderizan todos los widgets (segun el campo pasado)
            if field_type == "TEXT":
                component = ft.TextField(
                    label=field_name,
                    key=position,
                    disabled=field_read_only,
                    value=field_default
                )
                self.form_controls.append(component)

            elif field_type == "VARCHAR":
                component = ft.TextField(
                    label=field_name,
                    key=position,
                    disabled=field_read_only,
                    max_length=max_length,
                    value=field_default
                )
                self.form_controls.append(component)

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
                    disabled=field_read_only,
                    value=field_default
                )
                self.form_controls.append(component)

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
                    disabled=field_read_only,
                    value=field_default
                )
                self.form_controls.append(component)

            elif field_type == "BOOLEAN":
                VAL = field_default if field_default is not None else True
                component = ft.Switch(
                    label=field_name,
                    key=position,
                    disabled=field_read_only,
                    value=VAL
                )
                self.form_controls.append(component)

            elif field_type == "DATE":

                if field_read_only:
                    component = ft.TextField(
                        label=field_name,
                        key=position,
                        read_only=field_read_only,
                        value=field_default
                    )

                else:
                    picker = ft.DatePicker(
                        value=field_default
                    )
                    component = ft.Button(
                        content=field_name,
                        key=position,
                        disabled=field_read_only,
                        on_click=lambda e: self.page.show_dialog(picker),
                        icon=ft.Icons.CALENDAR_MONTH
                    )

                self.form_controls.append(component)

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
                        disabled=field_read_only,
                        value=field_default
                    )
                    self.form_controls.append(component)

                else:
                    self.date_picker.value = DATE
                    self.time_picker.value = TIME
                    date_component = ft.Button(
                        content=self.date_picker.value,
                        key=f"dia__{position}",
                        disabled=field_read_only,
                        on_click=lambda e:
                            self.page.show_dialog(date_picker),
                        icon=ft.Icons.CALENDAR_MONTH
                    )
                    time_component = ft.Button(
                        content=self.time_picker.value,
                        key=f"hora__{position}",
                        disabled=field_read_only,
                        on_click=lambda e:
                            self.page.show_dialog(time_picker),
                            icon=ft.Icons.TIMER
                    )

                    self.form_controls.append(date_component)    
                    self.form_controls.append(time_component)

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

                self.form_controls.append(component)

            else:
                raise TypeError(f"Unknown passed datatype {field_type}.")

        # Controles formulario de campo, fusion con controles estaticos.
        controls.extend(self.form_controls)

        # Boton de guardar
        controls.append(
            ft.Button(
                content="Guardar Cambios",
                key="save",
                icon=ft.Icons.SAVE,
                on_click=self.save_changes
            )
        )

        # Se declara una vista de scroll vertical para los formularios.
        self.form_widget = ft.ListView(
                controls=[
                    ft.Column(
                        controls=controls,
                        spacing=20,
                        expand=True
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
