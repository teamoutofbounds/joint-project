from django.core import management
from django.test import TestCase
from parameterized import parameterized
from django.core.exceptions import ValidationError
from magatzem.models import Room


class TestRoom(TestCase):

    def tearDown(self):
        management.call_command('flush', verbosity=0, interactive=False)

    @parameterized.expand([['Room 1', 0, 20, 0, 200, 0]])
    def test_room(self, name, temp, hum, quantity, limit, room_status):
        created = Room.objects.create(name=name, temp=temp, hum=hum,
                                      quantity=quantity, limit=limit,
                                      room_status=room_status)
        given = Room.objects.get(pk=created.pk)
        self.assertEqual(given.name, name)
        self.assertEqual(given.temp, temp)
        self.assertEqual(given.hum, hum)
        self.assertEqual(given.quantity, quantity)
        self.assertEqual(given.limit, limit)
        self.assertEqual(given.room_status, room_status)

    #   HUM TEST         HUM_MIN_VALUE = 0          HUM_MAX_VALUE = 100
    ###################################################################################

    @parameterized.expand([[0], [1], [10], [23], [38], [55], [78], [89], [99], [100]])
    def test_valid_hum(self, hum):
        created = Room.objects.create(name='Room', temp=0, hum=hum,
                                      quantity=0, limit=100,
                                      room_status=0)
        given = Room.objects.get(pk=created.pk)
        self.assertEqual(given.hum, hum)

    @parameterized.expand([[-1], [-10], [-100], [101], [123], [999]])
    def test_invalid_hum(self, hum):
        room = Room.objects.create(name='Room', temp=0, hum=hum,
                                   quantity=0, limit=100,
                                   room_status=0)
        with self.assertRaises(ValidationError):
            room.full_clean()
    #
    ###################################################################################

    #   TEMP TEST       TEMP_MIN_VALUE = -273       TEMP_MAX_VALUE = 100
    ###################################################################################

    @parameterized.expand([[-273], [-199], [-55], [-1], [0], [1], [10],
                           [23], [38], [55], [78], [89], [99], [100]])
    def test_valid_temp(self, temp):
        created = Room.objects.create(name='Room', temp=temp, hum=0,
                                      quantity=0, limit=100,
                                      room_status=0)
        given = Room.objects.get(pk=created.pk)
        self.assertEqual(given.temp, temp)

    @parameterized.expand([[-274], [-299], [-1000], [101], [120], [999]])
    def test_invalid_temp(self, temp):
        room = Room.objects.create(name='Room', temp=temp, hum=0,
                                   quantity=0, limit=100,
                                   room_status=0)
        with self.assertRaises(ValidationError):
            room.full_clean()
    #
    ###################################################################################

    #   STATUS TEST 0/1
    ###################################################################################

    @parameterized.expand([[0], [1]])
    def test_valid_status(self, status):
        created = Room.objects.create(name='Room', temp=0, hum=0,
                                      quantity=0, limit=100,
                                      room_status=status)
        given = Room.objects.get(pk=created.pk)
        self.assertEqual(given.room_status, status)

    @parameterized.expand([[-1], [-12], [-299], [2], [10], [999]])
    def test_invalid_temp(self, status):
        room = Room.objects.create(name='Room', temp=0, hum=0,
                                   quantity=0, limit=100,
                                   room_status=status)
        with self.assertRaises(ValidationError):
            room.full_clean()
