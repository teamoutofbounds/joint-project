import re
from django.db import models


class Container(models.Model):
    QUANTITY_MAX_VALUE = 1000000000
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
    SLA = models.IntegerField()

    def __init__(self, product_id, producer_id, limit, quantity, temp_min, temp_max, hum_min, hum_max, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self._has_product_id_correct_format(product_id) and \
           self._has_producer_id_correct_format(producer_id) and \
           self._has_limit_correct_format(limit) and \
           self._is_quantity_allowed(quantity) and \
           self._are_temperaures_allowed(temp_min, temp_max) and \
           self._are_humidity_allowed(hum_min, hum_max):

            self.product_id = product_id
            self.producer_id = producer_id
            self.limit = limit
            self.quantity = quantity
            self.temp_min = temp_min
            self.temp_max = temp_max
            self.hum_min = hum_min
            self.hum_max = hum_max
            self._set_service_level_agreement(limit)
        else:
            raise ValueError()

    def __str__(self):
        return Container.STR_PATTERN.format(self.product_id, self.producer_id, self.quantity, self.limit)

#   CHECKING PARAMETERS
#########################################################################################################

    def _has_product_id_correct_format(self, product_id):
        return isinstance(product_id, str) and re.match(r'^(\w ?)+$', product_id)

    def _has_producer_id_correct_format(self, producer_id):
        return isinstance(producer_id, str) and re.match(r'^(\d{11})$', producer_id)

    def _has_limit_correct_format(self, limit):
        return isinstance(limit, str) and re.match(r'^(\d{2}/\d{2}/\d{4})$', limit)

    def _is_quantity_allowed(self, quantity):
        return isinstance(quantity, int) and 0 < quantity < Container.QUANTITY_MAX_VALUE

    def _are_temperaures_allowed(self, temp_min, temp_max):
        return isinstance(temp_min, int) and isinstance(temp_max, int) and  \
               Container.TEMP_MIN_VALUE <= temp_min <= temp_max <= Container.TEMP_MAX_VALUE

    def _are_humidity_allowed(self, hum_min, hum_max):
        return isinstance(hum_min, int) and isinstance(hum_max, int) and \
               Container.HUM_MIN_VALUE <= hum_min <= hum_max <= Container.HUM_MAX_VALUE

##########################################################################################################
#

    def _set_service_level_agreement(self, limit):
        data = limit.split('/')
        self.SLA = int(data[2] + data[1] + data[0])
