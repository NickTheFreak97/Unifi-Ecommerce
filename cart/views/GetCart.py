from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from cart.models import Cart
from django_redis import get_redis_connection


class GetCart(APIView):
    permission_classes = [AllowAny]

    def perform_authentication(self, request):
        try:
            super().perform_authentication(request)
        except AuthenticationFailed:
            request._user = AnonymousUser()

    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.select_related('product').filter(user=request.user)

            if cart is not None:
                cart_in_response = [
                    {
                        "barcode": cart_item.product.barcode,
                        "quantity": cart_item.quantity,
                    }

                    for cart_item in cart
                ]

                return Response(
                    {
                        'cart': cart_in_response,
                    },
                    status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)
        else:
            guest_token = request.COOKIES.get('guest_token')

            if guest_token:
                redis = get_redis_connection("default")
                cart_mapping_hash = redis.hgetall(f"cart:{guest_token}")

                cart_mapping = {
                    barcode.decode(): quantity
                    for barcode,quantity in cart_mapping_hash.items()
                }

                cart_in_response = [
                    {
                        "barcode": barcode,
                        "quantity": cart_mapping[barcode],
                    }

                    for barcode in cart_mapping.keys()
                ]

                return Response(
                    {
                        'cart': cart_in_response,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(status=status.HTTP_402_PAYMENT_REQUIRED)