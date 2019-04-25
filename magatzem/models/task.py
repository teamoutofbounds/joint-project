from django.db import models, transaction
from .container import Container
from .room import Room
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from datetime import date

# from simple_history.models import HistoricalRecords


class Task(models.Model):
    MAX_TYPE_CHOICES_VALUE = 2
    TYPE_CHOICES = (
        (0, "Moviment d' Entrada"),
        (1, "Moviment Intern"),
        (2, "Moviment de Sortida"),
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

    description = models.CharField(max_length=32, verbose_name='Descripció')
    task_type = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_TYPE_CHOICES_VALUE)],
                                                 choices=TYPE_CHOICES, default=1, verbose_name='Tipus')
    task_status = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_STATUS_CHOICES_VALUE)],
                                                   choices=STATUS_CHOICES, default=0, verbose_name='Estat')
    origin_room = models.ForeignKey(Room, related_name='origin', on_delete=models.PROTECT, verbose_name="Sala d'origen")
    destination_room = models.ForeignKey(Room, related_name='destination', on_delete=models.PROTECT,
                                         verbose_name="Sala destí")
    containers = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True, verbose_name='Contenidor')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Persona assignada')

    date = models.DateField(default=date.today)
    # Contains all the changes of the object
    # history = HistoricalRecords()

    def __str__(self):
        return Task.STR_PATTERN.format(self.origin_room, self.destination_room, self.containers)

    @classmethod
    def assign_task(cls, user):
        with transaction.atomic():
            task = cls.objects.select_for_update().filter(task_status=0).first()
            if task and task.user is None:
                task.user = user
                # change status to automatically assigned
                task.task_status = 1
                task.save()
        return task
