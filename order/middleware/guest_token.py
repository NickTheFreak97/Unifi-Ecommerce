import uuid
from django.conf import settings

class GuestTokenMiddleware:
    affected_endpoints = [
        '/orders/create-order/',
        '/cart/create/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path in self.affected_endpoints and not (getattr(request, "user", None) and request.user.is_authenticated) and not request.COOKIES.get('guest_token'):
            print("Intercepted need for a guest token")
            guest_token = str(uuid.uuid4())
            request.COOKIES['guest_token'] = guest_token
            request.guest_token = guest_token

            response = self.get_response(request)

            response.set_cookie(
                'guest_token',
                guest_token,
                max_age=60 * 60 * 24, # 1 day
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                path="/",
            )

            return response
        else:
            return self.get_response(request)
