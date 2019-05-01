from behave import *
from magatzem.models import Room
from magatzem.models import Container

use_step_matcher("parse")


@step('There is a container "{container}" assigned to that room')
def step_impl(context, container):
    container = Room.objects.get(name=container)
    for row in context.table:
        for heading in row.headings:
            setattr(container, heading, row[heading])
        container.save()


@step('Exists a room named "{room_name}"')
def step_impl(context, room_name):
    room = Room.objects.get(name=room_name)
    for row in context.table:
        for heading in row.headings:
            setattr(room, heading, row[heading])
        room.save()


@when('I access to the data of room "{room_name}"')
def step_impl(context, room_name):
    room = Room.objects.get(name=room_name)
    context.browser.visit(context.get_url('magatzem:detail-room', room.pk))


@then('All the data of room "{room_name}" is correct for container "{container}"')
def step_impl(context, room_name, container):
    room = Room.objects.get(name=room_name)
    container = Container.objects.get(name=container)
    assert (container.temp_max <= room.temp) and (container.temp_min >= room.temp)
    assert (container.limit <= room.limit)
    assert (container.hum_max <= room.hum) and (container.hum_min >= room.hum)
    assert container.room == room.name
    assert container.quantity <= (room.limit - room.quantity)
    assert room.room_status is 0


@then('All the data of room "{room_name}" is NOT correct for container "{container}"')
def step_impl(context, room_name, container):
    room = Room.objects.get(name=room_name)
    container = Container.objects.get(name=container)
    assert (container.temp_max >= room.temp) and (container.temp_min <= room.temp)
    assert (container.limit >= room.limit)
    assert (container.hum_max >= room.hum) and (container.hum_min <= room.hum)
    assert container.room != room.name
    assert container.quantity >= (room.limit - room.quantity)
    assert room.room_status is 1
