from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q, Prefetch
from catalog.models import Category, Product

class Catalog(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        all_products_and_variants = (
            Product.objects
            .filter(
                Q(timeOfDeletion__isnull=True) | Q(timeOfDeletion__gt=timezone.now())
            )
            .prefetch_related("productvariant_set")
            .order_by("name")
        )

        all_categories_for_matching_products = (
            Category.objects.prefetch_related(
                Prefetch("product_set", queryset=all_products_and_variants)
            )
            .order_by("name")
        )

        home_view = [
            {
                "name": category.name,
                "products": [
                    {
                        "barcode": product.barcode,
                        "name": product.name,
                        "product_variants": [
                            {
                                "barcode": variant.barcode,
                                "unit_price": variant.unitPrice,
                                "stock": variant.stock,
                            }
                            for variant in product.productvariant_set.all()
                        ],
                    }
                    for product in category.product_set.all()
                ],
            }
            for category in all_categories_for_matching_products
        ]

        return Response(
            {
                'catalog': home_view,
            },
            status=status.HTTP_200_OK,
        )