from django.db import models
from .payment_strategy import PaymentStrategy


class CardPayment(PaymentStrategy):
    """
    Use this class to create a card payment method for a user.
    This maps 1:1 to a user's credit card payment method.

    Example:
        (f7e6d5c4-9b8a-7c6d-5ef4-3a2b1c0d9e8f, 'Mastercard', 0938, 2028-09-01 00:00:00+00, 'Niccolò Della Rocca')
    """
    network = models.CharField(max_length=15)
    last_4_digits = models.CharField(max_length=4)
    expiry_date = models.DateField()
    card_owner_name = models.CharField(max_length=63)