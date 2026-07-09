"""
URL configuration for Unifi_Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from cart.views import CreateCart, IncrementProduct, DecrementProduct, RemoveProduct, GetCart
from django.urls import path

urlpatterns = [
    path('create/', CreateCart.as_view(), name='create cart'),
    path('increment/', IncrementProduct.as_view(), name='increment product'),
    path('decrement/', DecrementProduct.as_view(), name='decrement product'),
    path('remove/', RemoveProduct.as_view(), name='remove product'),
    path('fetch/', GetCart.as_view(), name='fetch cart'),
]
