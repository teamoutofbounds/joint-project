from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from magatzem.models.product import Product
from magatzem.models.sla import SLA
from magatzem.models.manifest import Manifest


class ManifestContainer(models.Model):
    MANIFEST_CONTAINER_STR_PATTERN = "Manifest: {} Producte: {} Quantitat: {}"
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    id_product = models.ForeignKey(Product, unique=True, on_delete=models.PROTECT)
    id_SLA = models.ForeignKey(SLA, unique=True, on_delete=models.PROTECT)
    id_manifest = models.ForeignKey(Manifest, unique=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.MANIFEST_CONTAINER_STR_PATTERN.format(self.id_manifest, self.id_product, self.quantity)
