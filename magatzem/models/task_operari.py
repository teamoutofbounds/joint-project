from django.db import models, transaction
from .room import Room
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from magatzem.models.task import Task
from magatzem.models.container_group import ContainerGroup


class TaskOperari(Task):

    MAX_TYPE_CHOICES_VALUE = 2
    TYPE_CHOICES = (
        (0, "Moviment d' Entrada"),
        (1, "Moviment Intern"),
        (2, "Moviment de Sortida"),
    )

    task_type = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(MAX_TYPE_CHOICES_VALUE)],
        choices=TYPE_CHOICES, default=1, verbose_name='Tipus')

    origin_room = models.ForeignKey(
        Room, related_name='origin', on_delete=models.PROTECT,
        verbose_name="Sala d'origen")
    destination_room = models.ForeignKey(
        Room, related_name='destination', on_delete=models.PROTECT,
        verbose_name="Sala destí")
    containers = models.ForeignKey(ContainerGroup, on_delete=models.SET_NULL, null=True, verbose_name='Contenidor')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Persona assignada')

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
