from operator import itemgetter


# container hauria de ser un dictionary amb com a minim: producte, quantitat el producte que conte container hauria
# de ser un altre dictionary amb: id, temp_min, temp_max, humidity_max, humidity_min sales ha de ser una llista de
# sales on cada sala es un dictionary amb com a minim: stock_maxim, stock_restant, temperatura, humidity

def salaSelector(container, sales):
	container_list = []
	product = container['product']
	for sala in sales:
		if sala['stock_maxim'] - sala['stock_actual'] >= container['quantitat']:
			if product['temp_min'] <= sala['temperatura'] <= product['temp_max']:
				if product['humidity_min'] <= sala['humidity'] <= product['humidity_max']:
					sala['left_stock'] = sala['stock_maxim'] - sala[
						'stock_actual']  # Ja que no se si ho tenim a la base de dades ho faig aixi
					container_list.append(sala)

	return sorted(container_list, key=itemgetter('left_stock'))
# La de dalt es la primera versió que nomes fica els que compleixen les condicions i te les ordene.


# La de baix t'ho distribueix i afegeix una clau nova al dictionary de sala que distribueix els contenidors
# prioritzant l'aplenar sales

def salaSelectorv2(container, sales):
	container_list = []
	product = container['product']
	for sala in sales:
		if product['temp_min'] <= sala['temperatura'] <= product['temp_max']:
			if product['humidity_min'] <= sala['humidity'] <= product['humidity_max']:
				sala['left_stock'] = sala['stock_maxim'] - sala['stock_actual']
				sala['new_containers'] = 0
				container_list.append(sala)

	container_list = sorted(container_list, key=itemgetter('left_stock'))
	quantity = container['quantity']

	for sala in container_list:  # Ho recorrerem per els que tenen menys espai disponible.
		if quantity > 0:
			left_stock = sala['left_stock']
			if left_stock >= quantity:
				sala['left_stock'] -= quantity
				sala['new_containers'] = quantity
				quantity = 0
			elif left_stock < quantity:
				sala['new_containers'] = left_stock
				quantity -= left_stock
				sala['left_stock'] = 0
		else:
			break

	return container_list
