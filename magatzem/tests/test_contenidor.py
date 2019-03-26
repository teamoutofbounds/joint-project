from django.test import TestCase
from parameterized import parameterized
from magatzem.models import Container

#       CONTAINERS TESTS
###############################################################################################

class TestContainer(TestCase):

    @parameterized.expand([[None], [123], [{}], [""], ["."],
                          ["#%&#!Root"], [" "], ["  "]])
    def test_id_product_error(self, product_id):
        with self.assertRaises(ValueError):
            Container(product_id, '11111111111', '25/02/2019', 1, temp_min=1, temp_max=10, hum_min=10, hum_max=90)

    @parameterized.expand([[None], [[]], [{}], [""],
                          ["#%&#!#%&#"], ["Producer1"], ["1234567890"],
                           ["3456"], ["00034500"], ["12345678901234567890"],
                           [" 12345678901"], ["12345678901 "], ["12345 678901"],
                          [-11111111111], [123], [0000000000], [12345678901]])
    def test_id_producer(self, producer_id):
        with self.assertRaises(ValueError):
            Container("Apples", producer_id, '25/02/2019', 1, temp_min=1, temp_max=10, hum_min=10, hum_max=90)

    @parameterized.expand([[None], [[]], [{}], [""],
                          ["Quantity"], ["100"], ["123456789"],
                          [-2387], [-57], [-1], [0],
                           [1000000000], [98989898989]])
    def test_quantity(self, quantity):
        with self.assertRaises(ValueError):
            Container("Apples", '11111111111', '25/02/2019', quantity, temp_min=1, temp_max=10, hum_min=10, hum_max=90)

    @parameterized.expand(['25/02/19', '25/02', '25-02-2019'])
    def test_limit(self, limit):
        with self.assertRaises(ValueError):
            Container("Apples", '11111111111', limit, 1, temp_min=1, temp_max=10, hum_min=10, hum_max=90)

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [-1000], [-2869], [-65768], [-10000000]])
    def test_min_temp(self, temp_min):
        with self.assertRaises(ValueError):
            Container("Apples", '11111111111', '25/02/2019', 1, temp_min=temp_min, temp_max=10, hum_min=10, hum_max=90)

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [1000], [2869], [65768], [10000000]])
    def test_max_temp(self, temp_max):
        with self.assertRaises(ValueError):
            Container("Apples", '11111111111', '25/02/2019', 1, temp_min=1, temp_max=temp_max, hum_min=10, hum_max=90)

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [-10000], [-49], [-1]])
    def test_min_hum(self, hum_min):
        with self.assertRaises(ValueError):
            Container("Apples", '11111111111', '25/02/2019', 1, temp_min=1, temp_max=10, hum_min=hum_min, hum_max=90)

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [1000], [256], [101]])
    def test_max_hum(self, hum_max):
        with self.assertRaises(ValueError):
            Container("Apples", '11111111111', '25/02/2019', 1, temp_min=1, temp_max=10, hum_min=10, hum_max=hum_max)

    @parameterized.expand([[20, 10], [10, 0], [-5, -22], [100, -1],
                           [1000, 128], [-1, -2], [0, -1]])
    def test_temp_relation(self, temp_min, temp_max):
        with self.assertRaises(ValueError):
            Container("Apples", '11111111111', '25/02/2019', 1, temp_min=temp_min, temp_max=temp_max, hum_min=10, hum_max=90)

    @parameterized.expand([[100, 90],[20, 10], [10, 0],
                           [6, 5], [2, 1], [1, 0]])
    def test_hum_relation(self, hum_min, hum_max):
        with self.assertRaises(ValueError):
            Container("Apples", '11111111111', '25/02/2019', 1, temp_min=1, temp_max=10, hum_min=hum_min, hum_max=hum_max)

    @parameterized.expand([['t', '11111111111', 1],
                           ["Apples", '12312312312', 2],
                           ['Melon', '13313313313', 10],
                           ["MANZANA GREENTRANS", '92392392392', 154],
                           ["PERA CONFERENCE", '00000000000', 10648],
                           ["TABLONES CAOBA", '98979600000', 20678498]])
    def test_container_attrs(self, product_id, producer_id, quantity):
        container = Container(product_id=product_id, producer_id=producer_id, limit='25/02/2019', quantity=quantity,
                              temp_min=1, temp_max=10, hum_min=10, hum_max=90)
        self.assertEqual(container.product_id, product_id)
        self.assertEqual(container.producer_id, producer_id)
        self.assertEqual(container.quantity, quantity)

    @parameterized.expand([['01/12/2021', 20211201], ['25/02/2019', 20190225], ['30/01/2019', 20190130]])
    def test_container_SLA(self, limit, sla):
        container = Container(product_id='Apples', producer_id='11111111111', limit=limit, quantity=1,
                              temp_min=1, temp_max=10, hum_min=10, hum_max=90)
        self.assertEqual(container.SLA, sla)

    @parameterized.expand([["Apples", '11111111111', '25/02/2019', 1000, 1, 10, 10, 90],
                          ["Wood", '12345678900', '25/01/2021', 45, 200, 10, 15, 25, 35],
                          ["Pera conference", '28/12/2019', '78787878787', 1, 2, 6, 90, 100 ]])
    def container_str(self, product_id, producer_id, conditions_id, quantity):
        container = Container(product_id, producer_id, conditions_id, quantity)
        self.assertEqual(Container.STR_PATTERN.format(product_id, producer_id, quantity), container.__str__())

######################################################################################################
#