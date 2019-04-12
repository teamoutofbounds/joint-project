from django.core import management
from django.test import TestCase
from parameterized import parameterized
from magatzem.models import Container, Room
from django.core.exceptions import ValidationError


#       CONTAINERS TESTS
###############################################################################################


class TestContainer(TestCase):

    room = Room(name='Sala 1', temp_min=0, temp_max=100, hum_min=0, hum_max=100, quantity=10, limit=200, room_status=1)

    def setup(self):
        self.room.save()

    def tearDown(self):
        management.call_command('flush', verbosity=0, interactive=False)

#
########################################################################################################################
    """
        This tests are for Validators since django can't work with regular constructors...
        But for now can't be tested since by default django works with sqlite 
        that doesn't allow testing django validators.
        But don't worry, all is going to be easier with django...
    """
    '''
    @parameterized.expand([[None], [123], [{}], [""], ["."],
                           ["#%&#!Root"], [" "], ["  "]])
    def test_id_product_error(self, product_id):
        container = Container()
        with self.assertRaises(ValidationError):
            container.producer_id = product_id
    
    def test_id_producer_in_create(self, producer_id):
        container = Container()
        with self.assertRaises(ValidationError):
            container.producer_id = producer_id

    @parameterized.expand(['25/02/19', '25/02', '25-02-2019'])
    def test_limit(self, limit):
        container = Container()
        with self.assertRaises(ValidationError):
            container.limit = limit

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [-2387], [-57], [-1], [0],
                           [1000000000], [98989898989]])
    def test_quantity(self, quantity):
        container = Container()
        with self.assertRaises(ValidationError):
            container.quantity = quantity

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [-1000], [-2869], [-65768], [-10000000]])
    def test_min_temp_in_create(self, temp_min):
        container = Container()
        with self.assertRaises(ValidationError):
            container.temp_min = temp_min
            
    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [1000], [2869], [65768], [10000000]])
    def test_max_temp(self, temp_max):
        container = Container()
        with self.assertRaises(ValidationError):
            container.temp_max = temp_max

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [-10000], [-49], [-1]])
    def test_min_hum(self, hum_min):
        container = Container()
        with self.assertRaises(ValidationError):
            container.hum_min = hum_min

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [1000], [256], [101]])
    def test_max_hum(self, hum_max):
        container = Container()
        with self.assertRaises(ValidationError):
            container.hum_max = hum_max

    @parameterized.expand([[20, 10], [10, 0], [-5, -22], [100, -1],
                           [1000, 128], [-1, -2], [0, -1]])
    def test_temp_relation(self, temp_min, temp_max):
        container = Container()
        with self.assertRaises(ValidationError):
            container.temp_min = temp_min
            container.temp_max = temp_max

    @parameterized.expand([[100, 90], [20, 10], [10, 0],
                           [6, 5], [2, 1], [1, 0]])
    def test_hum_relation(self, hum_min, hum_max):
        container = Container()
        with self.assertRaises(ValidationError):
            container.hum_min = hum_min
            container.hum_max = hum_max

    def test_container_attrs(self, product_id, producer_id, quantity):
        container = Container()
        container.producer_id = producer_id
        container.producer_id = producer_id
        container.quantity = quantity
        self.assertEqual(container.product_id, product_id)
        self.assertEqual(container.producer_id, producer_id)
        self.assertEqual(container.quantity, quantity)

    @parameterized.expand([['01/12/2021', 20211201], ['25/02/2019', 20190225], ['30/01/2019', 20190130]])
    def test_container_SLA(self, limit, sla):
        container = Container()
        container.limit = limit
        self.assertEqual(container.get_sla(), sla)

    @parameterized.expand([["Apples", '11111111111', '25/02/2019', 1000, 1, 10, 10, 90],
                           ["Wood", '12345678900', '25/01/2021', 45, 200, 10, 15, 25, 35],
                           ["Pera conference", '28/12/2019', '78787878787', 1, 2, 6, 90, 100]])
    def container_str(self, product_id, producer_id, limit, quantity, temp_min, temp_max, hum_min, hum_max):
        container = Container()
        container.product_id = product_id
        container.producer_id = producer_id
        container.limit = limit
        container.quantity = quantity
        container.temp_min = temp_min
        container.temp_max = temp_max
        container.hum_min = hum_min
        container.hum_max = hum_max
        container.room = self.room
        self.assertEqual(Container.STR_PATTERN.format(product_id, producer_id, quantity), container.__str__())
    '''
########################################################################################################################
#
    """
        This test are for the static method that works like a container constructor 
        and allow us to test the container parameters.
    """
    @parameterized.expand([[None], [123], [{}], [""], ["."],
                          ["#%&#!Root"], [" "], ["  "]])
    def test_id_product_error_in_create(self, product_id):
        with self.assertRaises(ValueError):
            Container.create(product_id, '11111111111', '25/02/2019', 1, temp_min=1, temp_max=10,
                             hum_min=10, hum_max=90, room=self.room)

    @parameterized.expand([[None], [[]], [{}], [""],
                          ["#%&#!#%&#"], ["Producer1"], ["1234567890"],
                           ["3456"], ["00034500"], ["12345678901234567890"],
                           [" 12345678901"], ["12345678901 "], ["12345 678901"],
                          [-11111111111], [123], [0000000000], [12345678901]])
    def test_id_producer_in_create(self, producer_id):
        with self.assertRaises(ValueError):
            Container.create("Apples", producer_id, '25/02/2019', 1, temp_min=1, temp_max=10,
                             hum_min=10, hum_max=90, room=self.room)

    @parameterized.expand(['25/02/19', '25/02', '25-02-2019'])
    def test_limit_in_create(self, limit):
        with self.assertRaises(ValueError):
            Container.create("Apples", '11111111111', limit, 1, temp_min=1, temp_max=10,
                             hum_min=10, hum_max=90, room=self.room)

    @parameterized.expand([[None], [[]], [{}], [""],
                          ["Quantity"], ["100"], ["123456789"],
                          [-2387], [-57], [-1], [0],
                           [1000000000], [98989898989]])
    def test_quantity_in_create(self, quantity):
        with self.assertRaises(ValueError):
            Container.create("Apples", '11111111111', '25/02/2019', quantity, temp_min=1, temp_max=10,
                             hum_min=10, hum_max=90, room=self.room)

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [-1000], [-2869], [-65768], [-10000000]])
    def test_min_temp_in_create(self, temp_min):
        with self.assertRaises(ValueError):
            Container.create("Apples", '11111111111', '25/02/2019', 1, temp_min=temp_min, temp_max=10,
                             hum_min=10, hum_max=90, room=self.room)

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [1000], [2869], [65768], [10000000]])
    def test_max_temp_in_create(self, temp_max):
        with self.assertRaises(ValueError):
            Container.create("Apples", '11111111111', '25/02/2019', 1, temp_min=1, temp_max=temp_max,
                             hum_min=10, hum_max=90, room=self.room)

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [-10000], [-49], [-1]])
    def test_min_hum_in_create(self, hum_min):
        with self.assertRaises(ValueError):
            Container.create("Apples", '11111111111', '25/02/2019', 1, temp_min=1, temp_max=10,
                             hum_min=hum_min, hum_max=90, room=self.room)

    @parameterized.expand([[None], [[]], [{}], [""],
                           ["Quantity"], ["100"], ["123456789"],
                           [1000], [256], [101]])
    def test_max_hum_in_create(self, hum_max):
        with self.assertRaises(ValueError):
            Container.create("Apples", '11111111111', '25/02/2019', 1, temp_min=1, temp_max=10,
                             hum_min=10, hum_max=hum_max, room=self.room)

    @parameterized.expand([[20, 10], [10, 0], [-5, -22], [100, -1],
                           [1000, 128], [-1, -2], [0, -1]])
    def test_temp_relation_in_create(self, temp_min, temp_max):
        with self.assertRaises(ValueError):
            Container.create("Apples", '11111111111', '25/02/2019', 1, temp_min=temp_min, temp_max=temp_max,
                             hum_min=10, hum_max=90, room=self.room)

    @parameterized.expand([[100, 90], [20, 10], [10, 0],
                           [6, 5], [2, 1], [1, 0]])
    def test_hum_relation(self, hum_min, hum_max):
        with self.assertRaises(ValueError):
            Container.create("Apples", '11111111111', '25/02/2019', 1, temp_min=1, temp_max=10,
                             hum_min=hum_min, hum_max=hum_max, room=self.room)

    @parameterized.expand([['t', '11111111111', 1],
                           ["Apples", '12312312312', 2],
                           ['Melon', '13313313313', 10],
                           ["MANZANA GREENTRANS", '92392392392', 154],
                           ["PERA CONFERENCE", '00000000000', 10648],
                           ["TABLONES CAOBA", '98979600000', 20678498]])
    def test_container_attrs(self, product_id, producer_id, quantity):
        container = Container.create(product_id=product_id, producer_id=producer_id, limit='25/02/2019',
                                     quantity=quantity, temp_min=1, temp_max=10, hum_min=10, hum_max=90, room=self.room)
        self.assertEqual(container.product_id, product_id)
        self.assertEqual(container.producer_id, producer_id)
        self.assertEqual(container.quantity, quantity)

    @parameterized.expand([['01/12/2021', 20211201], ['25/02/2019', 20190225], ['30/01/2019', 20190130]])
    def test_container_SLA(self, limit, sla):
        container = Container.create(product_id='Apples', producer_id='11111111111', limit=limit, quantity=1,
                                     temp_min=1, temp_max=10, hum_min=10, hum_max=90, room=self.room)
        self.assertEqual(container.get_sla(), sla)

    @parameterized.expand([["Apples", '11111111111', '25/02/2019', 1000, 1, 10, 10, 90],
                          ["Wood", '12345678900', '25/01/2021', 45, 200, 10, 15, 25, 35],
                          ["Pera conference", '28/12/2019', '78787878787', 1, 2, 6, 90, 100]])
    def container_str(self, product_id, producer_id, limit, quantity, temp_min, temp_max, hum_min, hum_max):
        container = Container.create(product_id=product_id, producer_id=producer_id, limit=limit,
                                     quantity=quantity, temp_min=temp_min, temp_max=temp_max,
                                     hum_min=hum_min, hum_max=hum_max, room=self.room)
        self.assertEqual(Container.STR_PATTERN.format(product_id, producer_id, quantity), container.__str__())

######################################################################################################
#
