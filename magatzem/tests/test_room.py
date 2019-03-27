from django.core import management
from django.test import TestCase
from parameterized import parameterized
from magatzem.models import Room


class TestRoom(TestCase):

    def tearDown(self):
        management.call_command('flush', verbosity=0, interactive=False)

    @parameterized.expand([[None], [123], [{}], [""], ["."],
                           ["#%&#!Root"], [" "], ["  "]])
    def test_id_room_error(self, room_id):
        with self.assertRaises(ValueError):
            Room(id=1, name='Sala 1', temp_min=1, temp_max=10,
                 hum_min=10, hum_max=90, quantity=-50, limit=75, room_status=1)
