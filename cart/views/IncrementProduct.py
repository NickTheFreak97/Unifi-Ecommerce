from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, serializers
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.db.models import F
from cart.models import Cart
from django_redis import get_redis_connection


class IncrementProductSerializer(serializers.Serializer):
    barcode = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)


class IncrementProduct(APIView):
    permission_classes = [AllowAny]

    def perform_authentication(self, request):
        try:
            super().perform_authentication(request)
        except Exception:
            request._user = AnonymousUser()

    def put(self, request, *args, **kwargs):
        serializer = IncrementProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['barcode']
        quantity = serializer.validated_data['quantity']

        if request.user.is_authenticated:
            with transaction.atomic():
                product_to_update = Cart.objects.select_for_update().filter(
                    user=request.user,
                    product=product,
                )

                if product_to_update.exists():
                    product_to_update.update(quantity=F("quantity") + quantity)
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            guest_token = request.COOKIES.get('guest_token')

            if guest_token:
                redis = get_redis_connection('default')
                hash_code = f"cart:{guest_token}"

                redis.hincrby(hash_code, product, quantity)

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)