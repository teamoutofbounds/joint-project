import re
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from datetime import date
from magatzem.models import *


def validate_name(value):
    if not re.match(r'^(\w ?)+$', value):
        raise ValidationError(
            gettext_lazy('%(value) no es un nom valid.'),
            params={'value': value}
        )


def validate_ref(value):
    if not re.match(r'^(\d{11})$', value):
        raise ValidationError(
            gettext_lazy('%(value) no es una referencia de producte valida.'),
            params={'value': value}
        )


class Manifest(models.Model):
    MANIFEST_STR_PATTERN = "Ref: {} Date: {}"
    ref = models.CharField(validators=[validate_ref], max_length=11)
    # date = models.DateTimeField(default=date.today)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.MANIFEST_STR_PATTERN.format(self.ref, self.date)

    def _get_manifest_containers(self):
        from magatzem.models import ManifestContainer
        return ManifestContainer.objects.filter(id_manifest=self)
