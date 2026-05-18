from .. import models
from framework.datatable import DataTableORM
import flet as ft


def get_inventory():
    t_row, t_col = models.inventory.Inventory.all().raw(label=True)
    dataframe = ft.DataTable(
        columns = [ft.DataColumn(label=ft.Text(c)) for c in t_col],
        rows = [ft.DataRow(cells=[cell for cell in R]) for R in t_row]
        )
    return dataframe