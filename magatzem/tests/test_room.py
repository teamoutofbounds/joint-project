from django.core import management
from django.test import TestCase
from parameterized import parameterized
from magatzem.models import Room


class TestRoom(TestCase):

    def tearDown(self):
        management.call_command('flush', verbosity=0, interactive=False)

'''
    @parameterized.expand([[None], [123], [{}], [""], ["."],
                           ["#%&#!Root"], [" "], ["  "]])
    def test_id_room_error(self, room_id):
        with self.assertRaises(ValueError):
            Room(id=1, name='Sala 1', temp=10,
                 hum=90, quantity=-50, limit=75, room_status=1)
'''