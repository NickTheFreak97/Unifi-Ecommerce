import stripe
from django.contrib.auth.models import AnonymousUser
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from order.models import Order, OrderStatus
from django.db.models import Q


class create_payment_intent(APIView):

    permission_classes = [AllowAny]

    def perform_authentication(self, request):
        try:
            super().perform_authentication(request)
        except Exception:
            request._user = AnonymousUser()


    def post(self, request, *args, **kwargs):
        idempotency_key = request.data.get('idempotency_key')
        order_id = request.COOKIES.get('order')

        if not idempotency_key:
            return Response({
                "detail": "Please provide an idempotency key",
            }, status=HTTP_400_BAD_REQUEST)
        else:
            try:
                order = Order.objects.get(Q(user=request.user) & Q(id=order_id)) if request.user.is_authenticated else Order.objects.get(id=order_id)

                intent = stripe.PaymentIntent.create(
                    amount=order.price,
                    currency=order.currency,
                    metadata={
                        "user_id": request.user.id,
                        "order_id": order.id,
                    },
                    idempotency_key=idempotency_key,
                )

                return Response(
                    {"client_secret": intent.client_secret}
                )
            except Order.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except Exception:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
