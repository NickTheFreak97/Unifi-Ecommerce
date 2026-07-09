from django.contrib import admin
from django.urls import path, include
from .view import CreateOrder, CreateOrderFromCart

urlpatterns = [
    path('create_order/', CreateOrder.as_view(), name='create_order'),
    path('create_order_from_cart/', CreateOrderFromCart.as_view(), name='create_order_from_cart'),
]
