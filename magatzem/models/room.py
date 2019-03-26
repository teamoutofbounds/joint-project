from django.db import models
from django.core.validators import MaxValueValidator


class Room(models.Model):
    MAX_STATUS_CHOICES_VALUE = 1
    STATUS_CHOICES = (
        (0, "Tancada"),
        (1, "Oberta"),
    )
    STR_PATTERN = "Nom: {}\tEstat: {}\tMaxima capacitat: {}\tOcupat: {}"

    name = models.CharField(max_length=16)
    temp_min = models.SmallIntegerField()
    temp_max = models.SmallIntegerField()
    hum_min = models.PositiveSmallIntegerField()
    hum_max = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    quantity = models.PositiveIntegerField(default=0)
    limit = models.PositiveIntegerField()
    room_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0, validators=[MaxValueValidator(1)])

    class Meta:
        ordering = ['-room_status', 'name']

    def __str__(self):
        return Room.STR_PATTERN.format(self.name, self.room_status, self.limit, self.quantity)
