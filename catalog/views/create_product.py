from django.contrib.auth.models import PermissionsMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import json
import pycountry


from catalog.models.products.product import Product
from catalog.models.products.product_variant import ProductVariant

class CreateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        barcode = request.data.get('barcode')
        name = request.data.get('name')
        description = request.data.get('description')
        unit_price = request.data.get('price')
        currency = request.data.get('currency')
        stock = request.data.get('stock')

        datasheet = request.data.get('datasheet')
        category = request.data.get('category')

        if not request.user.has_perm('catalog.add_product') or not request.user.has_perm('catalog.add_productvariant'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            if barcode is None or name is None or description is None or unit_price is None or currency is None or stock is None:
                return Response(
                    {
                        'error': 'In order to create a product, you must specify at least a barcode, name, description, price, currency and stock'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if isinstance(datasheet, str):
                    try:
                        datasheet = json.loads(datasheet)
                    except (TypeError, ValueError):
                        return Response(
                            {
                                'error': 'Expected to receive a JSON-encoded string as datasheet',
                                'datasheet': datasheet
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                if isinstance(stock, float) and not stock.is_integer():
                    return Response(
                        {
                            'error': 'Stock field must be an integer. Got floating point instead.',
                            'stock': stock
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    try:
                        stock = int(stock)
                    except (TypeError, ValueError):
                        return Response(
                            {
                                'error': 'Stock is not a valid number',
                                'stock': stock
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    if stock < 0:
                        return Response(
                            {
                                'error': 'Stock cannot be negative',
                                'stock': stock
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                if len(currency) != 3:
                    return Response(
                        {
                            'error': 'Currency field must be a string of length 3.',
                            'currency': currency
                        }
                    )
                else:
                    if pycountry.currencies.get(alpha_3=currency) is None:
                        return Response(
                            {
                                'error': 'Currency is not a valid currency in the sense of ISO 4217.',
                                'currency': currency
                            }
                        )

                if not isinstance(unit_price, float) and not isinstance(unit_price, int):
                    return Response(
                        {
                            'error': 'Unit price must be a real number.'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    if unit_price < 0:
                        return Response(
                            {
                                'error': 'Unit price cannot be negative',
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )


                if Product.objects.filter(barcode=barcode).exists():
                    return Response(
                        {
                            'error': 'Product with this barcode already exists'
                        },
                        status.HTTP_400_BAD_REQUEST
                    )
                else:
                    created_product = Product.objects.create(
                        barcode=barcode,
                        name=name,
                        description=description,
                        datasheet=datasheet,
                        timeOfCreation=timezone.now(),
                        timeOfDeletion=None,
                        category_id=category
                    )

                    ProductVariant.objects.create(
                        barcode=barcode,
                        product=created_product,
                        unitPrice=unit_price,
                        priceCurrency=currency,
                        stock=stock
                    )

                    return Response(
                        {
                            'message': 'Successfully created a new product',
                            'product': barcode,
                            'category': category
                        },
                        status=status.HTTP_201_CREATED
                    )




