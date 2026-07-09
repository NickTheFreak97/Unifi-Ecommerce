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
        product = request.data.get('barcode')

        if product is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.user.is_authenticated:
                 Cart.objects.filter(
                    user=request.user,
                    barcode=product
                ).delete()

                 return Response(status=status.HTTP_200_OK)
            else:
                guest_token = request.COOKIES.get('guest_token')

                if guest_token:
                    redis = get_redis_connection('default')
                    hash_code = "$cart:{user_id}".format(user_id=guest_token)

                    redis.hdel(hash_code, product)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)