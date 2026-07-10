from cart.models import Cart
from catalog.models import ProductVariant
from django_redis import get_redis_connection, serializers
from rest_framework_simplejwt.authentication import JWTAuthentication


class CartMergingMiddleware:
    affected_endpoints = [
        '/cart/create/',
        '/cart/increment/',
        '/cart/decrement/',
        '/cart/remove/',
        '/cart/fetch/',
        '/cart/add/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def _get_jwt_user(self, request):
        try:
            jwt_auth = JWTAuthentication()
            auth_result = jwt_auth.authenticate(request)
            if auth_result:
                return auth_result[0]
        except Exception:
            pass
        return None

    def __call__(self, request):
        guest_token = request.COOKIES.get('guest_token')

        if (
            request.path in self.affected_endpoints
            and guest_token is not None
        ):
            user = self._get_jwt_user(request)

            if user and user.is_authenticated:
                redis = get_redis_connection('default')
                guest_cart_key = f'cart:{guest_token}'
                guest_cart = redis.hgetall(guest_cart_key)

                if guest_cart:
                    for barcode_bytes, quantity_bytes in guest_cart.items():
                        barcode = barcode_bytes.decode()
                        quantity = int(quantity_bytes.decode())

                        try:
                            product = ProductVariant.objects.get(barcode=barcode)
                        except ProductVariant.DoesNotExist:
                            continue

                        cart_item, created = Cart.objects.get_or_create(
                            user=user,
                            product=product,
                            defaults={'quantity': quantity},
                        )
                        if not created:
                            cart_item.quantity += quantity
                            cart_item.save()

                    redis.delete(guest_cart_key)

                response = self.get_response(request)
                response.delete_cookie('guest_token', path='/')
                return response

        return self.get_response(request)