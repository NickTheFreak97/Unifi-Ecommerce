from django.urls import path
from catalog.views import CreateCategory, CreateProduct

urlpatterns = [
    path('create_category/', CreateCategory.as_view(), name='create_category'),
    path('create/', CreateProduct.as_view(), name='create_product'),

]

