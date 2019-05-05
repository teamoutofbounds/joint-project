from django.core import management
from django.test import TestCase
from magatzem.models import ContainerGroup, Room, Product, SLA


class ContainerGroupTestCase(TestCase):

    def setUp(self):
        room = Room.objects.create(name='Room', temp=0,
                                   hum=0, quantity=10,
                                   limit=200, room_status=1)
        room.save()

        product = Product.objects.create(
            producer_id='Producer', product_id='Product')
        product.save()

        sla = SLA.objects.create(pk=0, limit='01/01/2020',
                                 temp_min=0, temp_max=0,
                                 hum_min=0, hum_max=0)
        sla.save()

        containers = ContainerGroup.objects.create(
            pk=0, quantity=10, id_room=room, id_product=product, sla=sla)
        containers.save()

    def tearDown(self):
        management.call_command('flush', verbosity=0, interactive=False)

    def test_container_group(self):
        containers = ContainerGroup.objects.get(pk=0)
        room = Room.objects.get(name='Room')
        product = Product.objects.get(product_id='Product')
        sla = SLA.objects.get(pk=0)
        self.assertEqual(containers.quantity, 10)
        self.assertEqual(containers.id_room, room)
        self.assertEqual(containers.id_product, product)
        self.assertEqual(containers.sla, sla)
