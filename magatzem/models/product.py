import re
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_name(value):
    if not re.match(r'^(\w ?)+$', value):
        raise ValidationError(
            gettext_lazy('%(value) no es un nom valid.'),
            params={'value': value}
        )


class Product(models.Model):
    STR_PATTERN = "Producte={} | Productor={}"
    product_id = models.CharField(validators=[validate_name], max_length=64)
    producer_id = models.CharField(validators=[validate_name], max_length=64)

    def __str__(self):
        return Product.STR_PATTERN.format(
            self.product_id, self.producer_id)
