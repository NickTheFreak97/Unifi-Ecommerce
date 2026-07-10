import uuid
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

class GuestTokenMiddleware:
    affected_endpoints = [
        '/orders/create-order/',
        '/cart/create/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def _get_jwt_user(self, request):
        try:
            auth_result = JWTAuthentication().authenticate(request)
            if auth_result:
                return auth_result[0]
        except Exception:
            pass
        return None

    def __call__(self, request):
        if (
                request.method == "POST"
                and request.path in self.affected_endpoints
                and not request.COOKIES.get('guest_token')
        ):
            user = self._get_jwt_user(request)
            if user and user.is_authenticated:
                return self.get_response(request)

            guest_token = str(uuid.uuid4())
            request.COOKIES['guest_token'] = guest_token
            request.guest_token = guest_token

            response = self.get_response(request)

            response.set_cookie(
                'guest_token',
                guest_token,
                max_age=60 * 60 * 24,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                path="/",
            )

            return response
        else:
            return self.get_response(request)