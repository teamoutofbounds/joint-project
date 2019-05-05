from django.test import TestCase
from parameterized import parameterized
from django.core.exceptions import ValidationError
from magatzem.models import SLA


class SLATestCase(TestCase):

    #   LIMIT TEST
    ###################################################################################

    @parameterized.expand(['03/01/2019', '25/02/2025', '30/10/2021'])
    def test_valid_limit(self, limit):
        created = SLA.objects.create(limit=limit,
                                     temp_min=0, temp_max=0,
                                     hum_min=0, hum_max=0)
        given = SLA.objects.get(pk=created.pk)
        self.assertEqual(given.limit, limit)

    @parameterized.expand(['25/02/19', '25/02', '25-02-2019'])
    def test_invalid_limit(self, limit):
        sla = SLA.objects.create(limit=limit,
                                 temp_min=0, temp_max=0,
                                 hum_min=0, hum_max=0)
        with self.assertRaises(ValidationError):
            sla.full_clean()

    #
    ###################################################################################

    #   HUM TEST         HUM_MIN_VALUE = 0          HUM_MAX_VALUE = 100
    ###################################################################################

    @parameterized.expand([[0], [1], [10], [23], [38], [55], [78], [89], [99], [100]])
    def test_valid_min_hum(self, min_hum):
        created = SLA.objects.create(limit='01/01/2020',
                                     temp_min=0, temp_max=0,
                                     hum_min=min_hum, hum_max=0)
        given = SLA.objects.get(pk=created.pk)
        self.assertEqual(given.hum_min, min_hum)

    @parameterized.expand([[0], [1], [10], [23], [38], [55], [78], [89], [99], [100]])
    def test_valid_max_hum(self, max_hum):
        created = SLA.objects.create(limit='01/01/2020',
                                     temp_min=0, temp_max=0,
                                     hum_min=0, hum_max=max_hum)
        given = SLA.objects.get(pk=created.pk)
        self.assertEqual(given.hum_max, max_hum)

    @parameterized.expand([[-1], [-10], [-100], [101], [123], [999]])
    def test_invalid_min_hum(self, min_hum):
        sla = SLA.objects.create(limit='01/01/2020',
                                 temp_min=0, temp_max=0,
                                 hum_min=min_hum, hum_max=0)
        with self.assertRaises(ValidationError):
            sla.full_clean()

    @parameterized.expand([[-1], [-10], [-100], [101], [123], [999]])
    def test_invalid_max_hum(self, max_hum):
        sla = SLA.objects.create(limit='01/01/2020',
                                 temp_min=0, temp_max=0,
                                 hum_min=0, hum_max=max_hum)
        with self.assertRaises(ValidationError):
            sla.full_clean()

    #
    ###################################################################################

    #   TEMP TEST       TEMP_MIN_VALUE = -273       TEMP_MAX_VALUE = 100
    ###################################################################################

    @parameterized.expand([[-273], [-199], [-55], [-1], [0], [1], [10],
                           [23], [38], [55], [78], [89], [99], [100]])
    def test_valid_mim_temp(self, min_temp):
        created = SLA.objects.create(limit='01/01/2020',
                                     temp_min=min_temp, temp_max=0,
                                     hum_min=0, hum_max=0)
        given = SLA.objects.get(pk=created.pk)
        self.assertEqual(given.temp_min, min_temp)

    @parameterized.expand([[-273], [-199], [-55], [-1], [0], [1], [10],
                           [23], [38], [55], [78], [89], [99], [100]])
    def test_valid_max_temp(self, max_temp):
        created = SLA.objects.create(limit='01/01/2020',
                                     temp_min=0, temp_max=max_temp,
                                     hum_min=0, hum_max=0)
        given = SLA.objects.get(pk=created.pk)
        self.assertEqual(given.temp_max, max_temp)

    @parameterized.expand([[-274], [-299], [-1000], [101], [120], [999]])
    def test_invalid_mim_temp(self, min_temp):
        sla = SLA.objects.create(limit='01/01/2020',
                                 temp_min=min_temp, temp_max=0,
                                 hum_min=0, hum_max=0)
        with self.assertRaises(ValidationError):
            sla.full_clean()

    @parameterized.expand([[-274], [-299], [-1000], [101], [120], [999]])
    def test_invalid_max_temp(self, max_temp):
        sla = SLA.objects.create(limit='01/01/2020',
                                 temp_min=0, temp_max=max_temp,
                                 hum_min=0, hum_max=0)
        with self.assertRaises(ValidationError):
            sla.full_clean()
    #
    ###################################################################################

    @parameterized.expand([['01/12/2021', 20211201], ['25/02/2019', 20190225], ['30/01/2019', 20190130]])
    def test_container_SLA(self, limit, sla):
        created = SLA.objects.create(limit=limit, hum_min=0, hum_max=0, temp_min=0, temp_max=0)
        given = SLA.objects.get(pk=created.pk)
        self.assertEqual(given.get_sla(), sla)

    @parameterized.expand([['01/12/2021', 0, 10, 20, 50],
                           ['25/01/2021', 5, 20, 50, 76],
                           ['28/12/2019', -28, -12, 20, 34]])
    def container_str(self, limit, temp_min, temp_max, hum_min, hum_max):
        created = SLA.objects.create(limit=limit, temp_min=temp_min, temp_max=temp_max,
                                     hum_min=hum_min, hum_max=hum_max)
        given = SLA.objects.get(created.pk)
        self.assertEqual(SLA.STR_PATTERN.format(
            limit, temp_min, temp_max, hum_min, hum_max),
            given.__str__())
