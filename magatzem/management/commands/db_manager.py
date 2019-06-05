import os
import re
from django.core.management.base import BaseCommand
# from magatzem.models import Container, Room, Task
from magatzem.models import Room, Product, SLA, ContainerGroup
from django.contrib.auth.models import Group, User

container_id = 0


class Command(BaseCommand):
    def handle(self, *args, **options):
        make_database()
        Group.objects.get_or_create(name='Gestor')
        Group.objects.get_or_create(name='Operari')
        Group.objects.get_or_create(name='Tecnic')
        Group.objects.get_or_create(name='CEO')
        group = Group.objects.get(name='Gestor')
        user = User.objects.get(username='admin')
        user.groups.add(group)


def make_database():
    path = os.getcwd()
    add_item(add_room, path + '/data/rooms.data')
    #add_item(add_product, path + '/data/product.data')
    #add_item(add_sla, path + '/data/sla.data')
    #add_item(add_containers_groups, path + '/data/containers.data')
    # add_item(add_container, path + '/data/containers.data')
    # add_item(add_task, path + '/data/tasks.data')


def add_item(func, filename):
    with open(filename, 'r') as file:
        for line in file.readlines():
            # if re.match(r'^*', line):
            #    continue
            params = line.split('|')
            func(params)


def add_room(params):
    room = Room(name=params[1], temp=params[2],
                hum=params[3], quantity=params[4],
                limit=params[5], room_status=params[6])
    room.id = params[0]
    room.save()


def add_product(params):
    product = Product(pk=params[0],
                      product_id=params[1],
                      producer_id=params[2])
    product.save()


def add_sla(params):
    sla = SLA(pk=params[0], limit=params[1],
              temp_min=params[2], temp_max=params[3],
              hum_min=params[3], hum_max=params[4])
    sla.save()


def add_containers_groups(params):
    # product|sla|room|quantity
    product = Product.objects.get(pk=params[0])
    sla = SLA.objects.get(pk=params[1])
    room = Room.objects.get(pk=params[2])
    container_group = ContainerGroup(id_product=product,
                                     id_room=room,
                                     sla=sla,
                                     quantity=params[3])
    container_group.save()


'''
def add_container(params):
    global container_id
    # room = Room.objects.get(params[-1])
    room = Room.objects.get(id=params[-1])
    container = Container(product_id=params[0], producer_id=params[1], limit=params[2],
                          temp_min=params[3], temp_max=params[4],
                          hum_min=params[5], hum_max=params[6],
                          quantity=params[7], room=room)
    container.pk = container_id
    container_id += 1
    container.save()
'''
'''
def add_task(params):
    # task.data
    # This file must contain the following fields:
    # description|task_type|task_status|origin_room|destination_room|product_id|producer_id|limit

    # container = Container.objects.filter(product_id=params[5], producer_id=params[6], limit=params[7]).first()
    # container = Container.objects.get(1)
    container = Container.objects.get(pk=params[5])
    task = Task(description=params[0], task_type=params[1], task_status=params[2],
                origin_room=Room.objects.get(id=params[3]), destination_room=Room.objects.get(id=params[4]),
                containers=container)
    task.save()
'''
