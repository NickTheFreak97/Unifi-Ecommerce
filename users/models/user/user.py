import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from payment.models import PaymentStrategy


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phoneNumber = models.CharField(max_length=15, null=True)
    streetAddress = models.CharField(max_length=127, null=True)
    zipCode = models.CharField(max_length=10, null=True)
    municipality = models.CharField(max_length=255, null=True)
    countryCode = models.CharField(max_length=2, null=True)
    sessionID = models.CharField(max_length=63)
    isVerified = models.BooleanField(default=False)
    preferred_payment_strategy = models.ForeignKey(
        PaymentStrategy,
        on_delete=models.CASCADE, # @TODO: Let's change this to SET_NULL, I don't wanna delete the user when the payment method changes.
        null=True,
        blank=True,
        related_name='preferred_payment_strategy_for_user'
    )