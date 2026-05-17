from .. import models

def get_inventory():
	import ipdb; ipdb.set_trace()
	row, col = models.inventory.Inventory.all().raw(label=True)
	res = (row, col)
	return res