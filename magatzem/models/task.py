from django.db import models
from .container import Container
from .room import Room
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator


class Task(models.Model):
    MAX_TYPE_CHOICES_VALUE = 2
    TYPE_CHOICES = (
        (0, "Entrada"),
        (1, "Intern"),
        (2, "Sortida"),
    )
    MAX_STATUS_CHOICES_VALUE = 4
    STATUS_CHOICES = (
        (0, "Pendent d'assignació"),
        (1, "Assignada automaticament"),
        (2, "Assignada manualment"),
        (3, "Rebuda"),
        (4, "Completada"),
    )
    STR_PATTERN = "Origin: {}\tDestination: {}\t Containers_info:\t {}"

    description = models.CharField(max_length=32)
    task_type = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_TYPE_CHOICES_VALUE)],
                                                 choices=TYPE_CHOICES, default=1)
    task_status = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_STATUS_CHOICES_VALUE)],
                                                   choices=STATUS_CHOICES, default=0)
    origin_room = models.ForeignKey(Room, related_name='origin', on_delete=models.PROTECT)
    destination_room = models.ForeignKey(Room, related_name='destination', on_delete=models.PROTECT)
    containers = models.ForeignKey(Container, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True)

    # Contains all the changes of the object
    history = HistoricalRecords()

    def __init__(self, description, task_type, task_status, origin_room, destination_room, containers, user,
                 history, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self._is_different_origin_destination(origin_room, destination_room) and self._is_allowed_choice(task_type) \
                and self._is_allowed_status(task_status) and self.is_allowed_user(user):

            self.description = description
            self.task_type = task_type
            self.task_status = task_status
            self.origin_room = origin_room
            self.destination_room = destination_room
            self.containers = containers
        else:
            raise ValueError()

    def __str__(self):
        return Task.STR_PATTERN.format(self.origin_room, self.destination_room, self.containers)

    def _is_different_origin_destination(self, origin, destination):
        return origin is not destination

    def _is_allowed_choice(self, choice):
        return 0 <= choice < 3

    def _is_allowed_status(self, status):
        return status == 0

    def is_allowed_user(self, user):
        return user.groups.filter(id=user.id, name='operari').exists()
