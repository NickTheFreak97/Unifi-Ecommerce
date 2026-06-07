from django.db import models
from .product_variant import ProductVariant


class ProductAttribute(models.Model):
    attribute = models.CharField(max_length=63, primary_key=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    value = models.CharField(max_length=63)