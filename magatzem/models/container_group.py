from django.db import models
from django.core.validators import MaxValueValidator
from magatzem.models import Room, Product, SLA


class ContainerGroup(models.Model):

    MAX_VALUE = 999
    STR_PATTERN = "SLA={} | Poducte={} | Productor={} | Sala={} | Quantitat={}"
    STATE = (
        (0, "unlock"),
        (1, "lock"),
    )

    quantity = models.PositiveSmallIntegerField(validators=[MaxValueValidator(MAX_VALUE)])
    id_room = models.ForeignKey(Room, on_delete=models.PROTECT)
    id_product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sla = models.ForeignKey(SLA, on_delete=models.PROTECT)
    state = models.PositiveSmallIntegerField(
        choices=STATE, default=0,
        validators=[MaxValueValidator(1)],
        verbose_name='Estat')

    def __str__(self):
        return ContainerGroup.STR_PATTERN.format(
            self.sla.limit,
            self.id_product.product_id,
            self.id_product.producer_id,
            self.id_room.name,
            self.quantity)

    def get_sla(self):
        return self.sla.get_sla()
