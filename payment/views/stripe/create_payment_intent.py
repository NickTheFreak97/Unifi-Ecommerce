import stripe
from django.contrib.auth.models import AnonymousUser
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from order.models import Order, OrderStatus
from django.db.models import Q
from payment.models import PaymentIntent
from payment.models.payment_intent import PaymentIntentStatus
from django.utils import timezone
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

class CreateStripePaymentIntent(APIView):

    permission_classes = [AllowAny]

    def perform_authentication(self, request):
        try:
            super().perform_authentication(request)
        except Exception:
            request._user = AnonymousUser()


    def post(self, request, *args, **kwargs):
        idempotency_key = request.data.get('idempotency_key')
        order_id = request.COOKIES.get('order')
        user_id = request.user.id if request.user.is_authenticated else request.COOKIES.get('guest_token') if request.COOKIES.get('guest_token') is not None else None

        if user_id is None:
            return Response(status=HTTP_401_UNAUTHORIZED)
        else:
            if not idempotency_key:
                return Response({
                    "detail": "Please provide an idempotency key",
                }, status=HTTP_400_BAD_REQUEST)
            else:
                try:
                    order = Order.objects.get(Q(user=request.user) & Q(id=order_id)) if request.user.is_authenticated else Order.objects.get(id=order_id)

                    intent = stripe.PaymentIntent.create(
                        amount=int(order.price * 100),
                        currency=order.currency,
                        metadata={
                            "user_id": user_id,
                            "order_id": order.id,
                        },
                        idempotency_key=idempotency_key,
                    )

                    payment_intent, created = PaymentIntent.objects.get_or_create(
                        provider_intent_id=intent.id,
                        defaults={
                            "order": order,
                            "provider": "stripe",
                            "status": PaymentIntentStatus.pending,
                            "amount": intent.amount,
                            "currency": intent.currency,
                            "time_of_creation": timezone.now(),
                            "time_of_last_update": timezone.now(),
                            "idempotency_key": idempotency_key,
                        }
                    )

                    return Response(
                        {
                            "client_secret": intent.client_secret,
                            "intent_id": payment_intent.id,
                            "stripe_intent_id": intent.id,
                        }
                    )
                except Order.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

