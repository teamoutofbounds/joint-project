from operator import itemgetter
from magatzem.models import Room


# Recordatori: Les sales han d'estar ordenades de menor a major 'left_stock'

class RoomHandler:
	def __init__(self, container, sales):
		self.container = container
		self.sales = sorted(sales, key=lambda k: k['left_stock'])
		self.quantity = container['qty']

	def select_containers(self):
		self._initialize_sales()
		room, less_quantity, more_quantity = self._get_exact_container_quantity()
		if room:
			return [room]
		return self._distribute_containers(less_quantity, more_quantity)

	# Comprovem si hi ha una sala amb exactament la mateixa capacitat disponible
	# que contenidors volem col·locar
	def _get_exact_container_quantity(self):
		for i, sala in enumerate(self.sales):
			if sala['left_stock'] == self.quantity:
				sala['new_containers'] = self.quantity
				return sala, None, None
			if sala['left_stock'] > self.quantity:
				less_quantity = self.sales[:i]
				more_quantity = self.sales[i:]
				return None, less_quantity, more_quantity

		return None, self.sales, None

	def _distribute_containers(self, less_quantity, more_quantity):
		if more_quantity:
			more_quantity[0]['left_stock'] -= self.quantity
			more_quantity[0]['new_containers'] = self.quantity
			self.quantity = 0
			return [more_quantity[0]]

		i = 0
		if less_quantity:
			while self.quantity > 0 and i < len(less_quantity):
				if self.quantity > less_quantity[i]['left_stock']:
					less_quantity[i]['new_containers'] = less_quantity[i]['left_stock']
					self.quantity -= less_quantity[i]['new_containers']
					i += 1
				else:
					less_quantity[i]['new_containers'] = self.quantity
					self.quantity = 0

		if self.quantity == 0:
			return less_quantity
		else:
			return []

	def _initialize_sales(self):
		for sala in self.sales:
			sala['new_containers'] = 0
