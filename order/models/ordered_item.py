from django.db import models
from .order import Order
from catalog.models.products import product
import uuid

class OrderedItem(models.Model):
    ordered_item_surrogate_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(product.Product, on_delete=models.CASCADE) # Products are soft-deleted, their entry is still in the db, so cascade delete never happens anyway.
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount_ordered = models.IntegerField()
    unit_price_at_purchase_time = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(unit_price_at_purchase_time__gt=0),
                name="unit_price_at_purchase_time_non_negative"
            ),

            models.UniqueConstraint(
                fields=('product', 'order'),
                name="ordered_item_actual_pk_product_order"
            )
        ]



