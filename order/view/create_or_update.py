from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .create import CreateOrderFromCart, UpdateOrder
from order.models import Order

class CreateOrUpdate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        order_id = request.COOKIES.get('order')

        if order_id is None:
            return CreateOrderFromCart.as_view()(request._request, *args, **kwargs)
        elif not Order.objects.filter(id=order_id).exists():
            response = CreateOrderFromCart.as_view()(request._request, *args, **kwargs)
            response.delete_cookie('order')
            return response
        else:
            return UpdateOrder.as_view()(request._request, *args, **kwargs)

    put = post
