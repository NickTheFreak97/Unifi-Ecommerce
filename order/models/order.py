from django.db import models
from django.db.models import TextChoices, constraints
import uuid

class OrderStatus(TextChoices):
    requires_confirmation = "requires_confirmation", "Waiting for confirmation on staff's end"
    paid = "paid", "Order paid"
    processing = "processing", "Order paid and waiting for shipment"
    shipped = "shipped", "Order shipped"
    succeeded = "succeeded", "Order was delivered successfully"
    canceled = "canceled", "Order canceled"
    action_required = "action_required", "Requested action on user's end"
    refund_requested = "refund_requested", "Customer requested refund"
    refunded = "refunded", "Customer refunded"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=False, related_name='orders')
    email = models.EmailField(default=None)
    status = models.CharField(max_length=21, choices=OrderStatus, default=OrderStatus.requires_confirmation)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3)
    shipping_street = models.CharField(max_length=127)
    street_zipcode = models.CharField(max_length=10)
    shipping_municipality = models.CharField(max_length=31)
    shipping_country = models.CharField(max_length=2)
    time_of_creation = models.DateField(auto_now_add=True)
    cart_hash = models.CharField(max_length=64, db_index=True, default=None, unique=True)
    guest_token = models.UUIDField(null=True, blank=True, db_index=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gt=0),
                name='order_price_non_negative'
            ),

            models.CheckConstraint(
                condition=(
                    models.Q(user__isnull=False, guest_token__isnull=True) |
                    models.Q(user__isnull=True, guest_token__isnull=False)
                ),
                name='no_duplicate_identity_for_user'
            ),
        ]


