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
        serializer = CartItemSerializer(data=request.data.get('cart', []), many=True)
        serializer.is_valid(raise_exception=True)

        validated_cart = serializer.validated_data

        if request.user.is_authenticated:
            added = []
            updated = []

            with transaction.atomic():
                for cart_item in validated_cart:
                    product = cart_item['barcode']
                    quantity= cart_item['quantity']

                    product_in_cart_model = Cart.objects.select_for_update().filter(
                        Q(product=product) & Q(user=request.user)
                    )

                    if product_in_cart_model is not None:
                        product_in_cart_model.update(quantity=quantity)
                        updated.append(product.barcode)
                    else:
                        Cart.objects.create(
                            user=request.user,
                            product=product,
                            quantity=quantity
                        )

                        added.append(product.barcode)


            return Response({
                'added': added,
                'updated': updated,
            }, status=status.HTTP_200_OK)
        else:
            guest_token = request.COOKIES.get('guest_token')
            if guest_token:
                redis = get_redis_connection("default")
                key_for_this_user = f"cart:{guest_token}"

                if redis.exists(key_for_this_user):
                    added = []
                    updated = []

                    for cart_item in validated_cart:
                        barcode = cart_item['barcode'].barcode
                        quantity= cart_item['quantity']

                        if barcode is None or quantity is None:
                            print("Bad format")
                            return Response(status=status.HTTP_400_BAD_REQUEST)
                        else:
                            if redis.hexists(key_for_this_user, barcode):
                                redis.hset(key_for_this_user, barcode, quantity)
                                updated.append(barcode)
                            else:
                                redis.hset(key_for_this_user, barcode,quantity)
                                added.append(barcode)

                    redis.expire(key_for_this_user, 60 * 60 * 24)
                    return Response({
                        'added': added,
                        'updated': updated,
                    }, status=status.HTTP_200_OK)
                else:
                    mapping = {
                        cart_item['barcode'].barcode: cart_item['quantity']
                        for cart_item in validated_cart
                    }

                    redis.hset(key_for_this_user, mapping=mapping)
                    redis.expire(key_for_this_user, 60 * 60 * 24)
                    return Response(status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'You don\'t  have a guest token and are not logged in' }, status=status.HTTP_400_BAD_REQUEST)