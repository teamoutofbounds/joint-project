import re
from django.db import models


class Container(models.Model):
    QUANTITY_MAX_VALUE = 999999999
    HUM_MIN_VALUE = 0
    HUM_MAX_VALUE = 100
    TEMP_MIN_VALUE = -999
    TEMP_MAX_VALUE = 999
    STR_PATTERN = "{} [{}] unitats:{} - SLA:{}"

    product_id = models.CharField(max_length=64)
    producer_id = models.CharField(max_length=64)
    limit = models.CharField(max_length=10)
    temp_min = models.IntegerField()
    temp_max = models.IntegerField()
    hum_min = models.IntegerField()
    hum_max = models.IntegerField()
    quantity = models.IntegerField()

    def __init__(self, product_id, producer_id, limit, quantity, temp_min, temp_max, hum_min, hum_max):
        if not isinstance(product_id, str) or not re.match(r'^(\w ?)+$', product_id):
            raise ValueError()
        if not isinstance(producer_id, str) or not re.match(r'^(\d{11})$', producer_id):
            raise ValueError()
        if not isinstance(limit, str) or not re.match(r'^(\d{2}/\d{2}/\d{4})$', limit):
            raise ValueError()
        if not isinstance(quantity, int) or quantity < 1 or quantity > Container.QUANTITY_MAX_VALUE:
            raise ValueError()
        if not isinstance(temp_min, int) or temp_min < Container.TEMP_MIN_VALUE:
            raise ValueError()
        if not isinstance(temp_max, int) or temp_max > Container.TEMP_MAX_VALUE:
            raise ValueError()
        if not isinstance(hum_min, int) or hum_min < Container.HUM_MIN_VALUE:
            raise ValueError()
        if not isinstance(hum_max, int) or hum_max > Container.HUM_MAX_VALUE:
            raise ValueError()
        if temp_min > temp_max:
            raise ValueError()
        if hum_min > hum_max:
            raise ValueError()

        self.product_id = product_id
        self.producer_id = producer_id
        self.limit = limit
        self.quantity = quantity
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.hum_min = hum_min
        self.hum_max = hum_max

    def __str__(self):
        return Container.STR_PATTERN.format(self.product_id, self.producer_id, self.quantity, self.limit)
