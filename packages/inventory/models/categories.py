from pancakes.models.model import PanCakesORM
from pancakes.sql import datatype


class Categories(PanCakesORM):
    _table = "categories"
    _depends = "self"

    # Campos
    name = datatype.Char(comment="Nombre Categoria", required=True, unique=True)
