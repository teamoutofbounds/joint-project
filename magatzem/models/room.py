from django.db import models
from django.core.validators import MaxValueValidator


class Room(models.Model):
    MAX_STATUS_CHOICES_VALUE = 1
    STATUS_CHOICES = (
        (0, "Tancada"),
        (1, "Oberta"),
    )
    STR_PATTERN = ""

    temp_min = models.PositiveIntegerField()
    temp_max = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    hum_min = models.PositiveIntegerField()
    hum_max = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    quantity = models.PositiveIntegerField(default=0)
    limit = models.PositiveIntegerField()
    room_status = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(1)])

    class Meta:
        ordering = ['room_status']
