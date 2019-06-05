from django.test import TestCase

from tools.algorithms.sala_selector import RoomHandler


class TestSalaSelector(TestCase):

	def setUp(self):
		self.container = {'temp_min': 15, 'temp_max': 25, 'humidity_max': 10, 'humidity_min': 60, 'qty': 20}

	def test_unique_room(self):
		sales = [{'stock_maxim': 100, 'left_stock': 5, 'temperatura': 20, 'humidity': 40},
				{'stock': 100, 'left_stock': 10, 'temperatura': 20, 'humidity': 40},
				{'stock': 100, 'left_stock': 20, 'temperatura': 20, 'humidity': 40},
				{'stock': 100, 'left_stock': 30, 'temperatura': 20, 'humidity': 40}]
		handler = RoomHandler(self.container, sales)

		correct_room = [{'stock': 100, 'left_stock': 20, 'temperatura': 20, 'humidity': 40, 'new_containers': 20}]
		self.assertEqual(handler.select_containers(), correct_room)

	def test_equal_divided(self):
		sales = [{'stock': 100, 'left_stock': 5, 'temperatura': 20, 'humidity': 40, 'new_containers': 0},
				{'stock': 100, 'left_stock': 5, 'temperatura': 20, 'humidity': 40, 'new_containers': 0},
				{'stock': 100, 'left_stock': 5, 'temperatura': 20, 'humidity': 40, 'new_containers': 0},
				{'stock': 100, 'left_stock': 5, 'temperatura': 20, 'humidity': 40, 'new_containers': 0}]
		handler = RoomHandler(self.container, sales)

		self.assertEqual(handler.select_containers(), [{'stock': 100, 'left_stock': 5, 'temperatura': 20, 'humidity': 40, 'new_containers': 5},
				{'stock': 100, 'left_stock': 5, 'temperatura': 20, 'humidity': 40, 'new_containers': 5},
				{'stock': 100, 'left_stock': 5, 'temperatura': 20, 'humidity': 40, 'new_containers': 5},
				{'stock': 100, 'left_stock': 5, 'temperatura': 20, 'humidity': 40, 'new_containers': 5}])

	def test_no_solution(self):
		sales = [{'stock': 100, 'left_stock': 1, 'temperatura': 20, 'humidity': 40, 'new_containers': 0},
				{'stock': 100, 'left_stock': 1, 'temperatura': 20, 'humidity': 40, 'new_containers': 0},
				{'stock': 100, 'left_stock': 1, 'temperatura': 20, 'humidity': 40, 'new_containers': 0},
				{'stock': 100, 'left_stock': 1, 'temperatura': 20, 'humidity': 40, 'new_containers': 0}]
		handler = RoomHandler(self.container, sales)

		self.assertEqual(handler.select_containers(), [])

	def test_one_room_bigger(self):
		sales = [{'stock': 100, 'left_stock': 2, 'temperatura': 20, 'humidity': 40, 'new_containers': 0},
				{'stock': 100, 'left_stock': 4, 'temperatura': 20, 'humidity': 40, 'new_containers': 0},
				{'stock': 100, 'left_stock': 8, 'temperatura': 20, 'humidity': 40, 'new_containers': 0},
				{'stock': 100, 'left_stock': 80, 'temperatura': 20, 'humidity': 40, 'new_containers': 0}]
		handler = RoomHandler(self.container, sales)

		self.assertEqual(handler.select_containers(), [{'stock': 100, 'left_stock': 60, 'temperatura': 20, 'humidity': 40, 'new_containers': 20}])
