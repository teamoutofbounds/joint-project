from django.db import models
from magatzem.models.manifest import Manifest


class ManifestEntrance(Manifest):
    origin = models.CharField(max_length=64, help_text="Productor d'origen")

    def __str__(self):
        return super().__str__() + "Origen: {}".format(self.origin)
