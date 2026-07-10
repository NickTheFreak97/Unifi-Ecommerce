from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, serializers
from django.db import transaction
from cart.models import Cart
from django_redis import get_redis_connection


class AddProductSerializer(serializers.Serializer):
    barcode = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)


class AddProduct(APIView):
    permission_classes = [AllowAny]

    def perform_authentication(self, request):
        try:
            super().perform_authentication(request)
        except Exception:
            request._user = AnonymousUser()

    def put(self, request, *args, **kwargs):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        barcode = serializer.validated_data['barcode']
        quantity = serializer.validated_data['quantity']

        if request.user.is_authenticated:
            with transaction.atomic():
                existing_entry = Cart.objects.select_for_update().filter(
                    user=request.user,
                    barcode=barcode,
                )
                created = False

                if existing_entry.exists():
                    existing_entry.update(quantity=quantity)
                else:
                    Cart.objects.create(
                        user=request.user,
                        barcode=barcode,
                        quantity=quantity,
                    )
                    created = True

            return Response(status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        else:
            guest_token = request.COOKIES.get('guest_token')
            if guest_token is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            redis = get_redis_connection('default')
            cart_key = f"cart:{guest_token}"

            redis.hset(cart_key, barcode, quantity)
            redis.expire(cart_key, 60 * 60 * 24)

            return Response(status=status.HTTP_201_CREATED)