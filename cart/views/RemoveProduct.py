from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from cart.models import Cart
from django_redis import get_redis_connection


class RemoveProduct(APIView):
    permission_classes = [AllowAny]

    def perform_authentication(self, request):
        try:
            super().perform_authentication(request)
        except Exception:
            request._user = AnonymousUser()

    def delete(self, request, *args, **kwargs):
        product = request.data.get("barcode")

        if product is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
            deleted, _ = Cart.objects.filter(
                user=request.user,
                product__barcode=product,
            ).delete()

            return Response(
                status=(
                    status.HTTP_204_NO_CONTENT
                    if deleted > 0
                    else status.HTTP_404_NOT_FOUND
                )
            )

        guest_token = request.COOKIES.get("guest_token")

        if guest_token:
            redis = get_redis_connection("default")
            hash_code = f"cart:{guest_token}"

            removed = redis.hdel(hash_code, product)

            if redis.hlen(hash_code) <= 0:
                redis.delete(hash_code)

            return Response(
                status=(
                    status.HTTP_204_NO_CONTENT
                    if removed > 0
                    else status.HTTP_404_NOT_FOUND
                )
            )

        return Response(status=status.HTTP_401_UNAUTHORIZED)