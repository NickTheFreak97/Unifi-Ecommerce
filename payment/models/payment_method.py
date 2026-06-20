from django.db import models
import uuid

class PaymentMethodTypes(models.TextChoices):
    card = "card", "Card"
    bank = "bank", "Bank"
    wallet = "wallet", "Wallet"

class PaymentMethod(models.Model):
    """
    This class is used to log the payment methods. It is independent of orders and users.
    An example of valid payment method:

    (a1b2c3d4-0001-0001-0001-000000000001, card, visa, stripe)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=15, null=False, blank=False, choices=PaymentMethodTypes)
    name = models.CharField(max_length=15, null=False, blank=False)
    provider = models.CharField(max_length=15)

    class Meta:
        unique_together = ('type', 'name','provider')
