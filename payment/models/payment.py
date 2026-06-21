from django.db import models
import uuid

from .payment_intent import PaymentIntent

# Consider adding a FK to Order to reduce the join cost to fetch the order associated with this payment instance
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    intent = models.ForeignKey(PaymentIntent, on_delete=models.CASCADE)
    time_of_settlement = models.DateTimeField(auto_now_add=True)
