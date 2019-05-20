from django.db import models
from django.core.validators import MaxValueValidator
from magatzem.models import *


class ManifestContainer(models.Model):
    MAX_VALUE = 999
    MANIFEST_CONTAINER_STR_PATTERN = "Manifest: {} Producte: {} Quantitat: {}"
    quantity = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(MAX_VALUE)])
    id_product = models.ForeignKey(Product, on_delete=models.PROTECT)
    id_SLA = models.ForeignKey(SLA, on_delete=models.PROTECT)
    id_manifest = models.ForeignKey(Manifest, on_delete=models.PROTECT)

    def __str__(self):
        return self.MANIFEST_CONTAINER_STR_PATTERN.format(
            self.id_manifest, self.id_product, self.quantity)
