from pancakes.models.model import PanCakesORM
from pancakes.sql import datatype


class Inventory(PanCakesORM):
    _table = "inventory"
    _depends = ["categories"]

    name = datatype.Char(comment="Nombre Producto", readonly=False)
    qty = datatype.Int(comment="Cantidad Stock", default=10)
    price = datatype.Float(comment="Precio Producto")
    saleable = datatype.Bool(comment="Es Vendible")
    extras = datatype.Text(comment="Notas Extras")
    sold = datatype.TimeStamp(comment="Fecha Hora Venta")
    registry = datatype.Date(comment="Fecha Ingreso")
    categories_id = datatype.ForeignKey(
        comment="Producto Categoria M:1",
        second_table="categories",
        column_id="categories_id",
    )
