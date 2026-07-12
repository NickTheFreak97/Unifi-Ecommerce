from django.db import models
from django.db.models import TextChoices
from order.models import Order
import uuid

class PaymentIntentStatus(TextChoices):
    requires_payment_method = 'requires_payment_method', 'Intent created, payment method not selected or declined'
    requires_challenge = 'requires_challenge', 'PSP requested a user challenge'
    pending = 'pending', 'Waiting for async work from PSP'
    success = 'Success', 'Payment completed successfully'
    aborted = 'aborted', 'Payment abandoned by the user'


class PaymentIntent(models.Model):
    """
    A payment intent is associated with the idea that the user **wants** to move forward with the order,
    but the order and relative payment intent are only created when the customer taps 'Pay Now' or equivalent CTA on the front-end.

    At this point, the server sorts the list of items (currently I imagine it as a tuple of (product_id, amount), subject to change),
    and creates a fingerprint out of it, for example making a JSON dump of the list and encoding via SHA256.

    The first time a user taps the CTA, an order is created, products are cloned into Ordered Item, and a Payment Intent with a new Idempotency key is created.
    As a good practice, it might be a good idea to reserve the stock for a timeframe, for example decrement the amount from the products stock temporarily,
    then fire a job that restores the stock amount and deletes the order and relative data if the user didn't complete within the window.

    The endpoint sends the order_id to the user, and every subsequent hit to the endpoint will have to include this field in the request body.
    If a request without an order_id is received, we can try a fallback mechanic that goes something like this:

    - We establish a timeframe, for example via Environment file, say for example 1 hour.
    - We look for orders that are not yet completed from the user, within the time frame

    If no order from this user was ever created and completed in the timeframe then we create a new order.
    If another order from this user was created and completed, we run a diff test with respect to all the candidates

    If at least one candidate matches the cart hash, we merge, else, we create a new order.

    A user could have two tabs open in the same browser or even use two different devices to complete the payment.
    This merge strategy defends us from failure to complete the order (potential money loss).

    A periodic job on Celery could clean up pending orders that were abandoned. For example every 15 minutes a periodic task
    executes and flips every order that is pending | requires_challenge to abandonded, and restores stocks.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    provider = models.CharField(max_length=15)
    provider_intent_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=31, choices=PaymentIntentStatus, default=PaymentIntentStatus.requires_payment_method)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_last_update = models.DateTimeField(auto_now=True)
    idempotency_key = models.CharField(max_length=36, null=True, blank=True, unique=True)


