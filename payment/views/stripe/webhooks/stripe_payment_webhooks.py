import stripe
import os

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from datetime import date
import calendar

from payment.models import CardPayment, Payment, PaymentIntent, PaymentMethod, PaymentMethodTypes
from payment.models.payment_intent import PaymentIntentStatus
from order.models import Order, OrderStatus
from users.models.user.user import User

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                os.environ.get('STRIPE_WEBHOOK_SECRET')
            )

        except ValueError:
            return Response(
                {"error": "Invalid payload"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except stripe.error.SignatureVerificationError:
            return Response(
                {"error": "Invalid signature"},
                status=status.HTTP_400_BAD_REQUEST
            )


        event_type = event["type"]

        if event_type == "payment_intent.succeeded":
            self.payment_succeeded(
                payment_intent=event["data"]["object"],
                idempotency_key=event["request"]["idempotency_key"]
            )

        elif event_type == "payment_intent.payment_failed":
            self.payment_failed(
                payment_intent=event["data"]["object"],
                idempotency_key=event["request"]["idempotency_key"]
            )

        elif event_type == "charge.refunded":
            self.payment_refunded(
                event["data"]["object"]
            )


        return Response(
            {"received": True},
            status=status.HTTP_200_OK
        )


    def payment_succeeded(
            self, payment_intent, idempotency_key):
        print("SUCCESS:", payment_intent["id"])


        charge = stripe.Charge.retrieve(payment_intent["latest_charge"])
        card = charge["payment_method_details"]["card"]

        last4 = card["last4"]
        network = card["brand"] if card["brand"] else card['network']
        name = charge["billing_details"]["name"] or "Unknown"
        expiry_date = date(card["exp_year"], card["exp_month"], calendar.monthrange(card["exp_year"], card["exp_month"])[1])

        payment_method = (
                PaymentMethod.objects.filter(type=PaymentMethodTypes.card, provider='stripe', name=network).first()
                or PaymentMethod.objects.filter(type=PaymentMethodTypes.card, provider='stripe').first()
        )

        if not payment_method:
            print("Could not fetch payment method for this")

        else:
            user_id = payment_intent["metadata"]["user_id"]
            user = User.objects.get(id=user_id) if user_id else None


            card_payment, created = CardPayment.objects.get_or_create(
                network=network,
                last_4_digits=last4,
                expiry_date=expiry_date,
                card_owner_name=name,
                defaults={
                    "method": payment_method,
                    "provider_token": card["fingerprint"] or payment_intent["payment_method"],
                    "user": user,
                    "isActive": True,
                },
            )

            try:
                payment_intent = PaymentIntent.objects.get(provider_intent_id=payment_intent["id"])


                payment = Payment.objects.create(
                    intent=payment_intent
                )

                payment_intent.status = PaymentIntentStatus.success
                payment_intent.time_of_last_update = timezone.now()
                payment_intent.save()

                order: Order = payment_intent.order
                order.status = OrderStatus.paid
                order.save()

            except PaymentIntent.DoesNotExist:
                print(f"Payment with idempotency_key ${idempotency_key} does not exist")
                raise PaymentIntent.DoesNotExist



    def payment_failed(self, payment_intent, idempotency_key):
        print(
            "FAILED:",
            payment_intent["id"]
        )

        try:
            payment_intent = PaymentIntent.objects.get(
                idempotency_key=idempotency_key
            )

            payment_intent.status = PaymentIntentStatus.requires_payment_method
            payment_intent.time_of_last_update = timezone.now()
            payment_intent.save()

            order: Order = payment_intent.order
            order.status = OrderStatus.action_required
            order.save()
        except PaymentIntent.DoesNotExist:
            print(f"Payment with idempotency_key ${idempotency_key} does not exist")
            raise PaymentIntent.DoesNotExist




    def payment_refunded(self, charge):
        print(
            "REFUNDED:",
            charge["id"]
        )

        stripe_intent_id = charge["payment_intent"]

        local_intent = PaymentIntent.objects.get(provider_intent_id=stripe_intent_id)
        order: Order = local_intent.order

        order.status = OrderStatus.refunded
        order.save()