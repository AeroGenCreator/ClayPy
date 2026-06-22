import flet as ft

from framework.new_datatable import DatatableORM

from .. import models


def get_inventory():
    model = models.inventory.Inventory
    return DatatableORM(
        model=model
        )

def get_categories():
    model = models.categories.Categories
    return DatatableORM(
        model=model
    )
