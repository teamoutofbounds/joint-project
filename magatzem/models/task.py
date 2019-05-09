from django.db import models
from django.core.validators import MaxValueValidator
from datetime import date


class Task(models.Model):

    MAX_STATUS_CHOICES_VALUE = 4
    STATUS_CHOICES = (
        (0, "Pendent d'assignació"),
        (1, "Assignada automaticament"),
        (2, "Assignada manualment"),
        (3, "Rebuda"),
        (4, "Completada"),
    )
    STR_PATTERN = "Descripcio: {} Estat: {} "

    description = models.CharField(max_length=32, verbose_name='Descripció')

    task_status = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_STATUS_CHOICES_VALUE)],
                                                   choices=STATUS_CHOICES, default=0, verbose_name='Estat')

    date = models.DateField(default=date.today)

    def __str__(self):
        return Task.STR_PATTERN.format(self.description, self._state)

    def get_status(self):
        return self.STATUS_CHOICES[self.task_status][1]
