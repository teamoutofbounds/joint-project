import os
import re
from django.core.management.base import BaseCommand
from magatzem.models import Container, Room, Task


class Command(BaseCommand):
    def handle(self, *args, **options):
        make_database()


def make_database():
    path = os.getcwd()
    add_item(add_room, path + '/data/rooms.data')
    add_item(add_container, path + '/data/containers.data')
    add_item(add_task, path + '/data/tasks.data')


def add_item(func, filename):
    with open(filename, 'r') as file:
        for line in file.readlines():
            '''
            if re.match('^*', line):
                continue
            '''
            params = line.split('|')
            func(params)


def add_room(params):
    room = Room(name=params[1], temp_min=params[2], temp_max=params[3],
                hum_min=params[4], hum_max=params[5], quantity=params[6],
                limit=params[7], room_status=params[8])
    room.id = params[0]
    room.save()


def add_container(params):
    # room = Room.objects.get(params[-1])
    room = Room.objects.get(id=params[-1])
    container = Container(product_id=params[0], producer_id=params[1], limit=params[2],
                          temp_min=params[3], temp_max=params[4],
                          hum_min=params[5], hum_max=params[6],
                          quantity=params[7], room=room)
    container.save()


def add_task(params):
    # task.data
    # This file must contain the following fields:
    # description|task_type|task_status|origin_room|destination_room|product_id|producer_id|limit

    container = Container.objects.filter(product_id=params[5], producer_id=params[6], limit=params[7]).first()
    # container = Container.objects.get(1)
    task = Task(description=params[0], task_type=params[1], task_status=params[2],
                origin_room=Room.objects.get(id=params[3]), destination_room=Room.objects.get(id=params[4]), containers=container)
    task.save()
