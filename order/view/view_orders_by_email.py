from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from order.models import Order

class OrdersByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False, allow_null=False)

class ViewOrdersByEmail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = OrdersByEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        orders = Order.objects.filter(Q(user__email=validated_data['email']) | Q(email=validated_data['email']))

        if orders.exists():
            order_objects = [
                {
                    'id': order.id,
                    'price': order.price,
                    'currency': order.currency,
                    'shipping_street': order.shipping_street,
                    'shipping_zipcode': order.street_zipcode,
                    'shipping_municipality': order.shipping_municipality,
                    'shipping_country': order.shipping_country,

                }

                for order in orders
            ]
            return Response({
                'orders': order_objects
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'orders': []
            }, status=HTTP_204_NO_CONTENT)




