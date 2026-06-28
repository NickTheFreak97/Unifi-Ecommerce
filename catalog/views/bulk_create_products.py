from django.db import transaction
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

import pycountry


from catalog.models import Product, ProductVariant, Category

class ProductSerializer(serializers.Serializer):
    barcode = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    stock = serializers.IntegerField()
    datasheet = serializers.JSONField()
    category = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Category.objects.all(),
    )

    def validate_price(self, unit_price):
        if unit_price <= 0:
            raise serializers.ValidationError("Unit price must be greater than 0")
        else:
            return unit_price

    def validate_stock(self, stock):
        if stock < 0:
            raise serializers.ValidationError("Stock must be at least 0")
        else:
            return stock

    def validate_currency(self, currency):
        if len(currency) != 3 or pycountry.currencies.get(alpha_3=currency.upper()) is None:
            raise serializers.ValidationError("Currency is not available or does not exist")
        else:
            return currency.upper()

class BulkProductsCreationSerializer(serializers.Serializer):
    products = ProductSerializer(many=True, allow_null=False, allow_empty=False)

    def validate_products(self, products):
        all_barcodes = [ product['barcode'] for product in products ]

        if len(all_barcodes) != len(set(all_barcodes)):
            raise serializers.ValidationError("Barcodes are not unique")
        else:
            return products


class BulkCreateProducts(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('catalog.add_product'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            bulk_creation_serializer = BulkProductsCreationSerializer(data=request.data)
            bulk_creation_serializer.is_valid(raise_exception=True)

            products_to_add = bulk_creation_serializer.validated_data['products']

            added_products = []
            skipped_products = []

            with transaction.atomic():
                for product in products_to_add:
                    created_product, was_created = Product.objects.get_or_create(
                        barcode=product['barcode'],
                        defaults={
                            'name': product['name'],
                            'description': product['description'],
                            'datasheet': product['datasheet'],
                            'timeOfCreation': timezone.now(),
                            'timeOfDeletion': None,
                            'category': product['category'],
                        }
                    )

                    if was_created:
                        added_products.append(created_product.barcode)

                        ProductVariant.objects.create(
                            barcode=product['barcode'],
                            product=created_product,
                            unitPrice=product['price'],
                            priceCurrency=product['currency'],
                            stock=product['stock']
                        )
                    else:
                        skipped_products.append(created_product.barcode)

            return Response(
                {
                    'created': added_products,
                    'skipped': skipped_products if len(skipped_products) > 0 else None,
                },
                status=status.HTTP_201_CREATED
            )