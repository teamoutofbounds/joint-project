from django.db import models
from magatzem.models import Room, Product, SLA


class ContainerGroup(models.Model):

    STR_PATTERN = "SLA={} | Poducte={} | Productor={} | Sala={} | Quantitat={}"

    quantity = models.PositiveSmallIntegerField(default=0)
    id_room = models.ForeignKey(Room, on_delete=models.PROTECT)
    id_product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sla = models.ForeignKey(SLA, on_delete=models.PROTECT)

    def __str__(self):
        return ContainerGroup.STR_PATTERN.format(
            self.sla.limit,
            self.id_product.product_id,
            self.id_product.producer_id,
            self.id_room.name,
            self.quantity)

    def get_sla(self):
        return self.sla.get_sla()
