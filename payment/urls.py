from django.urls import path
from .views import CreatePaymentMethod

urlpatterns = [
    path('create_method/', CreatePaymentMethod.as_view(), name='create_payment_method'),
]

