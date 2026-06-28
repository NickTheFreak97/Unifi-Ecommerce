from django.contrib import admin
from django.urls import path, include
from .view.create.create_order import CreateOrder

urlpatterns = [
    path('create_order/', CreateOrder.as_view()),
]
