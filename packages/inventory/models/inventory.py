from pancakes.models.model import PanCakesORM
from pancakes.sql import datatype


class Inventory(PanCakesORM):
    _table = "inventory"
    _depends = ["categories"]
    # _sql_constraints

    # Campos
    name = datatype.Char(
        comment="Nombre Producto",
        unique=True,
        required=True
    )
    quantity = datatype.Int("Cantidad Producto")
    price = datatype.Float("Precio Producto")