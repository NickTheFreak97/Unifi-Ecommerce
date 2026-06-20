from django.db import models
import uuid

from users.models.user import user
from payment.models.payment_method import PaymentMethod

class PaymentStrategy(models.Model):
    """
    This class is used to represent the user's payment strategy for an order or a preferred payment strategy.
    It is used as a base for table polymorphism, collecting all the fields that are common to card/wallet/bank payments.

    Example:
    (f7e6d5c4-9b8a-7c6d-5ef4-3a2b1c0d9e8f, a1b2c3d4-0001-0001-0001-000000000001, true, pm_10qX2KLkdlwHu7ixHmCbvZxP, 2026-06-20 16:49:10)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(user.User, on_delete=models.CASCADE)
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)
    provider_token = models.CharField(max_length=255)
    time_of_creation = models.DateTimeField(auto_now_add=True)
