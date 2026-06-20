from django.db import models
from .payment_strategy import PaymentStrategy

class BankPayment(PaymentStrategy):
    """
    Use this class to represent a bank payment strategy tied to a specific user.

    Example:
          ('b2c3d4e5-2222-4a2b-9c3d-000000000002', 'Intesa Sanpaolo', '7421', '2026-04-02 16:45:00+00');
    """
    bank_name = models.CharField(max_length=15)
    last_4_digits = models.CharField(max_length=4)
    time_of_verification = models.DateField(null=True, blank=True, default=None)