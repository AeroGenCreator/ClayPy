"""
Moldes Desarrollo:

Intanciar a partir de las siguientes clases permite empaquetar
componente (Flet - Logica Backend).

DataTableORM es capaz de desempaquetar estas instancias, acomodarlas en su
respectivo contenedor y renderizar widgets.

Esto conecta backend de un modulo con 'modelo' renderizado a travez de
DataTableORM.
"""
# Python
from dataclasses import dataclass
from typing import Callable, Dict, Optional

# ClayPy
from .datatable import DataTableORM


@dataclass
class SaveEntry:
    section: str  # Seccion del lienzo
    label: str  # Texto en el componente
    key: str  # Identificador unico
    function: Callable[[Dict, "DataTableORM"], None]  # Funcion on_click
    icon: Optional[str] = None  # Icono
