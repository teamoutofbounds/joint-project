from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from magatzem.models import ContainerGroup


class Room(models.Model):

    ROOMS_NAME = {
        '1': 'Sala 1', '2': 'Sala 2',
        'A': 'Sala A', 'B': 'Sala B', 'C': 'Sala C',
        'M1': 'M1', 'M2': 'M2', 'M3': 'M3', 'M4': 'M4',
        'F1': 'F1', 'F2': 'F2', 'F3': 'F3', 'F4': 'F4',
        'F5': 'F5', 'F6': 'F6', 'F7': 'F7', 'Moll': 'Moll'
    }
    MAX_STATUS_CHOICES_VALUE = 1
    STATUS_CHOICES = (
        (0, "Tancada"),
        (1, "Oberta"),
    )
    STR_PATTERN = "Nom: {}\tEstat: {}\tMaxima capacitat: {}\tOcupat: {}"

    name = models.CharField(max_length=16, default='Nova Sala', verbose_name='Nom')
    temp = models.SmallIntegerField(
        validators=[MinValueValidator(-273), MaxValueValidator(100)],
        verbose_name='Temperatura (ºC)')
    hum = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        verbose_name='Humitat (%)')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Espai ocupat')
    limit = models.PositiveIntegerField(verbose_name='Capacitat màxima')
    room_status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=0,
        validators=[MaxValueValidator(1)],
        verbose_name='Estat')

    '''
    class Meta:
        ordering = ['-room_status', 'name']
    '''

    def __str__(self):
        return Room.STR_PATTERN.format(self.name, self.room_status, self.limit, self.quantity)

    def get_name(self):
        return Room.ROOMS_NAME[self.name]

    def get_containers(self, _state=0):
        return ContainerGroup.objects.filter(id_room=self.id, state=_state)
