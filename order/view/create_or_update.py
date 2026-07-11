from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .create import CreateOrderFromCart, UpdateOrder

class CreateOrUpdate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if request.COOKIES.get('order') is None:
            print(f"Order cookie is not set -> new order")
            return CreateOrderFromCart.as_view()(request._request, *args, **kwargs)
        else:
            print(f"Order cookie is set -> update")
            return UpdateOrder.as_view()(request._request, *args, **kwargs)

    put = post