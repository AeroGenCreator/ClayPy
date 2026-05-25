"""
Moldes Desarrollo:

Intanciar a partir de las siguientes clases permite empaquetar
componente (Flet - Logica Backend).

DataTableORM es capaz de desempaquetar estas instancias, acomodarlas en su
respectivo contenedor y renderizar widgets.

Esto conecta backend de un modulo con 'modelo' renderizado a travez de
DataTableORM.
"""
from dataclasses import dataclass


@dataclass
class SaveEntry:
	label: str
	
