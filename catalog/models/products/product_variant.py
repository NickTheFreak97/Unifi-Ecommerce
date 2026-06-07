from django.db import models
from django.db.models import Q
from .product import Product

class ProductVariant(models.Model):
    barcode = models.CharField(max_length=127, unique=True, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    priceCurrency = models.CharField(max_length=3)
    stock = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(stock__gte=0),
                name="stock_non_negative"
            ),

            models.CheckConstraint(
                condition=Q(unitPrice__gte=0),
                name="unit_price_non_negative"
            )
        ]