from django.db import models
from .payment_strategy import PaymentStrategy

class WalletTypeChoices(models.TextChoices):
    balance = 'balance', 'Balance', # For example, PayPal balance, Revolut balance
    bank_linked = 'Bank linked', 'Bank linked', # For example Venmo
    tokenized_card = 'Tokenized card', 'Tokenized card', # For example Apple Pay, Google Pay
    bnpl = 'BNPL', 'Buy now, pay Later' # For example Klarna

class WalletPayment(PaymentStrategy):
    """
    Example:
          ('b2c3d4e5-3333-4a2b-9c3d-000000000003', 'tokenized_card', 'PayPal', 'niccolo.dellarocca@edu.unifi.it', 'WJZ6TROC0BLQB1', 'IT');
    """
    type = models.CharField(choices=WalletTypeChoices, max_length=15)
    provider = models.CharField(choices=WalletTypeChoices, max_length=15)
    email = models.EmailField(max_length=63)
    external_account_id = models.CharField(max_length=255)
    country_code = models.CharField(max_length=2) # ISO 3166-1 alpha-2 country name