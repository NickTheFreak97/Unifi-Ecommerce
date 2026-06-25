from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from catalog.models import ProductVariant

class RestockProduct(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        product = request.data.get('product_id', None)
        stock_refill = request.data.get('adding_stock', None)

        if request.user.has_perm('catalog.change_productvariant'):
            if product is None or stock_refill is None:
                return Response({
                        'message': 'Provide a product and a stock amount',
                        'product_id': product,
                        'stock_refill': stock_refill,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if stock_refill < 0:
                    return Response(
                        {
                            'message': 'Stock refill cannot be negative',
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    product_ref = ProductVariant.objects.get(barcode=product)

                    if product_ref is None:
                        return Response(
                            {
                                'message': 'Product not found',
                            },
                            status=status.HTTP_404_NOT_FOUND
                        )
                    else:
                        if not isinstance(stock_refill, int):
                            return Response(
                                {
                                    'message': 'Stock refill must be an integer'
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        else:
                            updated_stock = product_ref.stock + stock_refill
                            product_ref.stock += updated_stock
                            product_ref.save()


                            return Response({
                                    'product_id': product,
                                    'updated_stock_to': updated_stock,
                                },
                                status=status.HTTP_200_OK
                            )
        else:
            return Response(
                {
                    'message': 'You are not allowed to update the stock of a product',
                },
                status=status.HTTP_403_FORBIDDEN
            )
