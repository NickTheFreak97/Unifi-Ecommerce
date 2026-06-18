from django.urls import path
from catalog.views import CreateCategory

urlpatterns = [
    path('create_category/', CreateCategory.as_view(), name='create_category'),
]

