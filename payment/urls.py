from django.urls import path
from .views import CreatePaymentMethod, CreateStripePaymentIntent, StripeWebhookView

urlpatterns = [
    path('create_method/', CreatePaymentMethod.as_view(), name='create_payment_method'),
    path('stripe/intent/create/', CreateStripePaymentIntent.as_view(), name='create_payment_intent_for_stripe'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='web_hooks_for_stripe'),
]

