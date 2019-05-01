from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords


class Room(models.Model):
    MAX_STATUS_CHOICES_VALUE = 1
    STATUS_CHOICES = (
        (0, "Tancada"),
        (1, "Oberta"),
    )
    STR_PATTERN = "Nom: {}\tEstat: {}\tMaxima capacitat: {}\tOcupat: {}"

    name = models.CharField(max_length=16, default='Nova Sala', verbose_name='Nom')
    temp = models.SmallIntegerField(validators=[MinValueValidator(-273), MaxValueValidator(100)],
                                    verbose_name='Temperatura (ºC)')
    hum = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], verbose_name='Humitat (%)')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Espai ocupat')
    limit = models.PositiveIntegerField(verbose_name='Capacitat màxima')
    room_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0, validators=[MaxValueValidator(1)],
                                                   verbose_name='Estat')

    # Contains all the changes of the object
    history = HistoricalRecords()

    '''
    class Meta:
        ordering = ['-room_status', 'name']
    '''

    def __str__(self):
        return self.name

    # def __str__(self):
        # return Room.STR_PATTERN.format(self.name, self.room_status, self.limit, self.quantity)
