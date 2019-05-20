from django.test import TestCase
from parameterized import parameterized
from django.core.exceptions import ValidationError
from magatzem.models import Product


class ProductTestCase(TestCase):

    @parameterized.expand(['Productor', 'Productor 1', 'Productor dos', 'Productor següent'])
    def test_valid_producer(self, producer):
        created = Product.objects.create(producer_id=producer, product_id='Product')
        given = Product.objects.get(pk=created.pk)
        self.assertEqual(given.producer_id, producer)

    @parameterized.expand(['', ' ', ' Producer', '#Producer', '%&f7#@#'])
    def test_invalid_producer(self, producer):
        product = Product.objects.create(producer_id=producer, product_id='Product')
        with self.assertRaises(ValidationError):
            product.full_clean()

    @parameterized.expand(['Product', 'Product 1', 'Product dos', 'Product següent'])
    def test_valid_product(self, product):
        created = Product.objects.create(producer_id='Producer', product_id=product)
        given = Product.objects.get(pk=created.pk)
        self.assertEqual(given.product_id, product)

    @parameterized.expand(['', ' ', ' Product', '#Product', '%&f7#@#'])
    def test_invalid_product(self, product):
        product = Product.objects.create(producer_id='Producer', product_id=product)
        with self.assertRaises(ValidationError):
            product.full_clean()

    @parameterized.expand([['Producer', 'Product'],
                           ['Producer two', 'Product two'],
                           ['Producer següent', 'Producte següent']])
    def product_str(self, producer, product):
        created = Product.objects.create(producer_id=producer, product_id=product)
        given = Product.objects.get(created.pk)
        self.assertEqual(Product.STR_PATTERN.format(product, producer), given.__str__())
