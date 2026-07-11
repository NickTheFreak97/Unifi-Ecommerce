from django.urls import path
from .view import CreateOrder, CreateOrderFromCart, UpdateOrder, CreateOrUpdate

urlpatterns = [
    path('create_order/', CreateOrder.as_view(), name='create_order'),
    path('create_order_from_cart/', CreateOrderFromCart.as_view(), name='create_order_from_cart'),
    path('update_order/', UpdateOrder.as_view(), name='update_order'),
    path('create_or_update/', CreateOrUpdate.as_view(), name='create_or_update'),
]
