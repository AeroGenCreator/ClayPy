import flet as ft

from framework.datatable import DataTableORM

from .. import models


def get_inventory():
    model = models.inventory.Inventory
    return DataTableORM(
        model=model
        )
