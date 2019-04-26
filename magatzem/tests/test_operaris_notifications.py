'''
from django.core import management
from django.test import TestCase
from magatzem.models.container import Container
from magatzem.models.task import Task
from magatzem.models.room import Room
from magatzem.views import assign_task
from django.contrib.auth.models import User


class InitializeTest(object):
    def __init__(self, num_tasks):
        object.__init__(self)
        self.num_tasks = num_tasks
        self.tasks = []

    def run(self):
        self.origin, self.destination = self._create_rooms()
        self.container = self._create_container()
        self.user = self._create_user()

    def create_task(self, container, origin, destination):
        tasks = []
        for i in self.num_tasks:
            tasks.append(Task.objects.create(description='traslladar'+str(i), origin_room=origin,
                                             destination_room=destination, container=container))
        self.tasks = tasks

    def _create_rooms(self):
        origin = Room.objects.create(name='origin', temp=50, hum=80, quantity=5, limit=200)
        destination = Room.objects.create(name='destination', temp=50, hum=80, quantity=5, limit=200)
        return origin, destination

    def _create_container(self):
        container = Container.objects.create(product_id=1, producer_id=123, limit='01/12/2019', quantity=5,
                                             temp=10, hum=50, room=self.origin)
        return container

    def _create_user(self):
        user = User.objects.create(username='TestUser', password='12345678sdj')
        return user


class OperariAssignTaskTests(TestCase):

    def tearDown(self):
        management.call_command('flush', verbosity=0, interactive=False)

    def assign_task_no_tasks(self):
        test_conds = InitializeTest(0)

        result = assign_task(test_conds.user)
        self.assertEquals(result, None, 'No té el mateix tipus')

    def assign_task_one_task(self):
        test_conds = InitializeTest(1)

        result = assign_task(test_conds.user)
        self.assertEquals(result, None, msg='No té el mateix')
        self.assertEquals(result.user, test_conds.user, msg='No ha assignat correctament')
        self.assertEquals(result.task_status, 1, msg='No té mateix status')

    def assign_task_more_than_one_task(self):
        test_conds = InitializeTest(3)

        result = assign_task(test_conds.user)
        self.assertEquals(result, None, msg='No té el mateix')
        self.assertEquals(result.user, test_conds.user, msg='No ha assignat correctament')
        self.assertEquals(result.task_status, 1, msg='No té mateix status')
        self.assertEquals(result, test_conds.tasks[0], msg='No és la primera tasca')
'''
