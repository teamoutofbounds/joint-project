from operator import itemgetter
from magatzem.models import Room


# container hauria de ser un dictionary amb com a minim: producte, quantitat el producte que conte container hauria
# de ser un altre dictionary amb: id, temp_min, temp_max, humidity_max, humidity_min sales ha de ser una llista de
# sales on cada sala es un dictionary amb com a minim. Les sales s'han d'enviar amb les condicions correctes per el producte
# : stock_maxim, stock_restant, temperatura, humidity


class RoomHandler:
	def __init__(self, container, sales):
		self.container = container
		self.sales = sales
		self.quantity = container['quantity']

	def select_containers(self):
		room, less_quantity, more_quantity = self._get_exact_container_quantity
		if room:
			return [room]
		return self._distribute_containers(less_quantity, more_quantity)

	# Comprovem si hi ha una sala amb exactament la mateixa capacitat disponible
	# que contenidors volem col·locar
	def _get_exact_container_quantity(self):
		for i, sala in enumerate(self.sales):
			if sala['left_stock'] == self.quantity:
				sala['new_containers'] = self.quantity
				return sala
			if sala['left_stock'] > self.quantity:
				less_quantity = self.sales[:i]
				more_quantity = self.sales[i:]
				break
		return None, less_quantity, more_quantity

	def distribute_containers(self, less_quantity, more_quantity):
		if more_quantity:
			more_quantity[0]['left_stock'] -= self.quantity
			more_quantity[0]['new_containers'] = self.quantity
			self.quantity = 0
			return [more_quantity[0]]

		distribution_list = []
		i = 0
		while self.quantity > 0:
			if self.quantity < distribution_list['left_stock']:
				distribution_list['new_containers'] = self.quantity - distribution_list['left_stock']
				distribution_list['left_stock'] -= self.quantity
				self.quantity -= distribution_list['new_containers']
			else:
				distribution_list['new_containers'] = self.quantity
				self.quantity = 0
		if self.quantity == 0:
			return distribution_list
		else:
			return []
