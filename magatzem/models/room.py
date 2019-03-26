from django.db import models
from django.core.validators import MaxValueValidator


class Room(models.Model):
    MAX_STATUS_CHOICES_VALUE = 1
    STATUS_CHOICES = (
        (0, "Tancada"),
        (1, "Oberta"),
    )
    STR_PATTERN = ""

    name = models.CharField(max_length=16)
    temp_min = models.SmallIntegerField()
    temp_max = models.PositiveIntegerField()
    hum_min = models.PositiveIntegerField()
    hum_max = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    quantity_in_the_room = models.PositiveIntegerField(default=0)
    quantity_moving = models.SmallIntegerField(default=0)
    limit = models.PositiveIntegerField()
    room_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0, validators=[MaxValueValidator(1)])

    class Meta:
        ordering = ['-room_status', 'name']
