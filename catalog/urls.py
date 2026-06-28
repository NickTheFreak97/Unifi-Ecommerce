from django.urls import path
from catalog.views import CreateCategory, CreateProduct, RestockProduct, BulkCreateCategories, BulkCreateProducts

urlpatterns = [
    path('create_category/', CreateCategory.as_view(), name='create_category'),
    path('bulk_create_categories/', BulkCreateCategories().as_view(), name='bulk_create_categories'),
    path('create/', CreateProduct.as_view(), name='create_product'),
    path('bulk_create/', BulkCreateProducts.as_view(), name='bulk_create_product'),
    path('restock/', RestockProduct.as_view(), name='restock_product'),
]

