from django.urls import path
from catalog.views import CreateCategory, CreateProduct, RestockProduct
urlpatterns = [
    path('create_category/', CreateCategory.as_view(), name='create_category'),
    path('create/', CreateProduct.as_view(), name='create_product'),
    path('restock/', RestockProduct.as_view(), name='restock_product'),
]

