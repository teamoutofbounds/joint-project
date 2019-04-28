import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from magatzem.models.room import Room


def validate_products(value):
    if not re.match(r'^(\w ?)+$', value):
        raise ValidationError(
            gettext_lazy('%(value) no es un nom de producte.'),
            params={'value': value}
        )


def validate_client(value):
    if not re.match(r'^(\d{11})$', value):
        raise ValidationError(
            gettext_lazy('%(value) no és un identificador de client vàlid.'),
            params={'value': value}
        )


def validate_limit(value):
    if not re.match(r'^(\d{2}/\d{2}/\d{4})$', value):
        raise ValidationError(
            gettext_lazy('%(value) no és un Level Service Agreement vàlid.'),
            params={'value': value}
        )


class Container(models.Model):
    QUANTITY_MAX_VALUE = 999999999
    HUM_MIN_VALUE = 0
    HUM_MAX_VALUE = 100
    TEMP_MIN_VALUE = -273
    TEMP_MAX_VALUE = 100
    STR_PATTERN = "{} [{}] unitats:{} - SLA:{}"

    product_id = models.CharField(validators=[validate_products], max_length=64)
    producer_id = models.CharField(validators=[validate_client], max_length=11)
    limit = models.CharField(validators=[validate_limit], max_length=10)
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(QUANTITY_MAX_VALUE)])
    temp = models.IntegerField(validators=[MinValueValidator(TEMP_MIN_VALUE), MaxValueValidator(TEMP_MAX_VALUE)])
    hum = models.IntegerField(validators=[MinValueValidator(HUM_MIN_VALUE), MaxValueValidator(HUM_MAX_VALUE)])
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    SLA = models.IntegerField(default=0)

    # NO SE SI ES NECESSARI

    #def clean(self):
        #if self.temp_min > self.temp_max:
            #raise ValidationError(gettext_lazy(
                #'La temperatura mínima d\'un contenedor no pot ser superior a la temperatura màxima.'))
        #if self.hum_min > self.hum_max:
            #raise ValidationError(gettext_lazy(
                #'La humitat mínima d\'un contenedor no pot ser superior a la humitat màxima.'))

    def get_sla(self):
        if self.SLA == 0:
            self._set_service_level_agreement()
        return self.SLA

    @staticmethod
    def create(product_id, producer_id, limit, quantity, temp, hum, room):
        if Container._has_product_id_correct_format(product_id) and \
                Container._has_producer_id_correct_format(producer_id) and \
                Container._has_limit_correct_format(limit) and \
                Container._is_quantity_allowed(quantity) and \
                Container._are_temperaures_allowed(temp) and \
                Container._are_humidity_allowed(hum):
            container = Container(product_id=product_id, producer_id=producer_id, limit=limit,
                                  quantity=quantity, temp=temp, hum=hum, room=room)
            return container
        else:
            raise ValueError()

    def __str__(self):
        return Container.STR_PATTERN.format(self.product_id, self.producer_id, self.quantity, self.limit)

#   CHECKING PARAMETERS
#########################################################################################################

    @staticmethod
    def _has_product_id_correct_format(product_id):
        return isinstance(product_id, str) and re.match(r'^(\w ?)+$', product_id)

    @staticmethod
    def _has_producer_id_correct_format(producer_id):
        return isinstance(producer_id, str) and re.match(r'^(\d{11})$', producer_id)

    @staticmethod
    def _has_limit_correct_format(limit):
        return isinstance(limit, str) and re.match(r'^(\d{2}/\d{2}/\d{4})$', limit)

    @staticmethod
    def _is_quantity_allowed(quantity):
        return isinstance(quantity, int) and 0 < quantity <= Container.QUANTITY_MAX_VALUE

    @staticmethod
    def _are_temperature_allowed(temp):
        return isinstance(temp, int) and  \
               Container.TEMP_MIN_VALUE <= temp <= Container.TEMP_MAX_VALUE

    @staticmethod
    def _are_humidity_allowed(hum):
        return isinstance(hum, int)  and \
               Container.HUM_MIN_VALUE <= hum <= Container.HUM_MAX_VALUE

##########################################################################################################
#

    def _set_service_level_agreement(self):
        data = self.limit.split('/')
        self.SLA = int(data[2] + data[1] + data[0])
