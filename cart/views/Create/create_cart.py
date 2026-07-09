from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from .cart_item_serializer import CartItemSerializer
from django_redis import get_redis_connection
from cart.models import Cart
class CreateCart(APIView):
    permission_classes = [AllowAny]

    def perform_authentication(self, request):
        try:
            super().perform_authentication(request)
        except Exception:
            request._user = AnonymousUser()

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_cart = serializer.validated_data

        if request.user.is_authenticated:
            added = []
            updated = []

            with transaction.atomic():
                for product, amount in validated_cart.items():
                    product_in_cart_model = Cart.objects.select_for_update().filter(
                        Q('product__eq', product.barcode) & Q('user__eq', request.user)
                    )

                    if product_in_cart_model is not None:
                        product_in_cart_model.update(amount=amount)
                        updated.append(product.barcode)
                    else:
                        Cart.objects.create(
                            user=request.user,
                            product=product,
                            amount=amount
                        )

                        added.append(product.barcode)


            return Response({
                'message': 'You are logged in',
                'added': added,
                'updated': updated,
            }, status=status.HTTP_200_OK)
        else:
            guest_token = request.COOKIES.get('guest_token')
            if guest_token:
                redis = get_redis_connection("default")
                key_for_this_user = f"cart:{guest_token}"

                if redis.exists(key_for_this_user):
                    return Response(
                        {'detail': 'Cart was already created'},
                        status=status.HTTP_409_CONFLICT,
                    )
                else:
                    mapping = {
                        barcode: amount
                        for barcode, amount in validated_cart.items()
                    }

                    redis.hset("inventory", mapping=mapping)
                    redis.expire(key_for_this_user, 60 * 60 * 24)
                    return Response(status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'You don\'t  have a guest token and are not logged in' }, status=status.HTTP_400_BAD_REQUEST)