import re
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.core.validators import MinValueValidator, MaxValueValidator


def validate_limit(value):
    if not re.match(r'^(\d{4}-\d{2}-\d{2})$', value):
        raise ValidationError(
            gettext_lazy('%(value) no és un Level Service Agreement vàlid.'),
            params={'value': value}
        )


class SLA(models.Model):
    HUM_MIN_VALUE = 0
    HUM_MAX_VALUE = 100
    TEMP_MIN_VALUE = -273
    TEMP_MAX_VALUE = 100
    STR_PATTERN = "Limit={} | Tmin={} Tmax={} | Hmin={} Hmax{}"

    limit = models.CharField(validators=[validate_limit], max_length=10)
    temp_min = models.IntegerField(validators=[MinValueValidator(TEMP_MIN_VALUE),
                                               MaxValueValidator(TEMP_MAX_VALUE)])
    temp_max = models.IntegerField(validators=[MinValueValidator(TEMP_MIN_VALUE),
                                               MaxValueValidator(TEMP_MAX_VALUE)])
    hum_min = models.IntegerField(validators=[MinValueValidator(HUM_MIN_VALUE),
                                              MaxValueValidator(HUM_MAX_VALUE)])
    hum_max = models.IntegerField(validators=[MinValueValidator(HUM_MIN_VALUE),
                                              MaxValueValidator(HUM_MAX_VALUE)])
    SLA = models.IntegerField(default=0)

    def __str__(self):
        return SLA.STR_PATTERN.format(
            self.limit, self.temp_min, self.temp_max, self.hum_min, self.hum_max)

    def get_sla(self):
        if self.SLA == 0:
            self._set_service_level_agreement()
        return self.SLA

    def _set_service_level_agreement(self):
        data = self.limit.split('-')
        self.SLA = int(data[0]) + int(data[1]) + int(data[2])
