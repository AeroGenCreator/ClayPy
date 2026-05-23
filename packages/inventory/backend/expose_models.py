from .. import models
from framework.datatable import DataTableORM
import flet as ft


def get_inventory():
    container = models.inventory.Inventory.all().container(label=True)
    return DataTableORM(container=container)