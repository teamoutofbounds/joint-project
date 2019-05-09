from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
from magatzem.models.manifest_container import ManifestContainer


class Manifest(models.Model):
    MANIFEST_STR_PATTERN = "Ref: {} Date: {}"
    ref = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), ])
    date = models.DateTimeField(default=date.today)

    def __str__(self):
        return self.MANIFEST_STR_PATTERN.format(self.ref, self.date)

    def _get_manifest_containers(self):
        return ManifestContainer.objects.filter(id_manifest=self)
