import os
from django.core.management.base import BaseCommand
from magatzem.models import Container, Room


class Command(BaseCommand):
    def handle(self, *args, **options):
        make_database()


def make_database():
    path = os.getcwd()
    # PRIMER S'HAN DE CREAR LES SALES
    # *******************************
    # add_rooms(path + '/data/rooms.data')
    # add_containers(path + '/data/containers.data')
    # add_tasks(path + '/data/tasks.data')


def add_containers(filename):
    with open(filename, 'r') as file:
        for line in file.readlines():
            params = line.split('|')
            add_container(params)


def add_container(params):
    room = Room.objects.get(params[-1])
    container = Container(product_id=params[0], producer_id=params[1], limit=params[2],
                          temp_min=params[3], temp_max=params[4],
                          hum_min=params[5], hum_max=params[6],
                          quantity=params[7], room=room)
    container.save()

