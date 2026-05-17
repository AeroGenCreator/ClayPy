from .. import models


def get_inv_raw():
    row, col = models.inventory.Inventory.all().raw(label=True)
    res = col
    return res

def get_inv_dicc():
    return models.inventory.Inventory.all().to_dict(label=True)

def get_inv_json():
    return models.inventory.Inventory.all().to_json(label=True)
