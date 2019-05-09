from django.db import models
from .room import Room
from django.core.validators import MaxValueValidator
from magatzem.models.task import Task


class TaskTecnic(Task):
    MAX_TYPE_CHOICES_VALUE = 2
    TYPE_CHOICES = (
        (0, "Manteniment"),
        (1, "Avaria"),
        (2, "Ajust"),
    )

    task_type = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_TYPE_CHOICES_VALUE)],
                                                 choices=TYPE_CHOICES, default=1, verbose_name='Tipus')

    detail = models.CharField(max_length=250)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)











