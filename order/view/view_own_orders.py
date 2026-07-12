from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q
from order.models import Order

class ViewOwnOrders(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        guest_token = request.COOKIES.get("guest_token")

        if not request.user.is_authenticated and guest_token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(
            Q(user=request.user) if request.user.is_authenticated
            else Q(guest_token=guest_token)
        ).order_by("time_of_creation")

        if not orders.exists():
            return Response({
                'orders': []
            }, status=HTTP_204_NO_CONTENT)
        else:
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



