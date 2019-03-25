from operator import itemgetter


# container hauria de ser un dictionary amb com a minim: producte, quantitat el producte que conte container hauria
# de ser un altre dictionary amb: id, temp_min, temp_max, humidity_max, humidity_min sales ha de ser una llista de
# sales on cada sala es un dictionary amb com a minim: stock_maxim, stock_restant, temperatura, humidity

def salaSelectorv2(container, sales):
	container_list = []
	product = container['product']
	for sala in sales:
		if is_room_suitable(product, sala):
			sala['left_stock'] = sala['stock_maxim'] - sala['stock_actual']
			sala['new_containers'] = 0
			container_list.append(sala)

	container_list = sorted(container_list, key=itemgetter('left_stock'), reverse=True)  # S'ordena descentment
	quantity = container['quantity']

	for sala in container_list:  # Comprovem si hi ha una sala amb exactament la mateixa capacitat disponible
		if sala['left_stock'] == quantity:  # que contenidors volem col·locar
			sala['new_containers'] = quantity
			return container_list

	for sala in container_list:
		if quantity > 0:
			left_stock = sala['left_stock']
			if left_stock > quantity:
				sala['left_stock'] -= quantity
				sala['new_containers'] = quantity
				quantity = 0
			elif left_stock < quantity:
				sala['new_containers'] = left_stock
				quantity -= left_stock
				sala['left_stock'] = 0
		else:
			return container_list

	if quantity == 0:  # En el cas que en l'última sala pot haver distribuit tots els contenidors l'if no faria el return
		return container_list

	return []  # S'hi s'arriba aquí significa que no hi ha solució per les sales obertes disponibles


def is_room_suitable(product, sala):
	return product['temp_min'] <= sala['temperatura'] <= product['temp_max'] and \
		product['humidity_min'] <= sala['humidity'] <= product['humidity_max']
