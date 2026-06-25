from datetime import timedelta

import pycountry
from django.db import models
from django.db.models import Q
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .create_order_serializer import CreateOrderSerializer
from order.utils.CartHash import cart_hash
import os
from order.models import Order, OrderStatus
from django_countries.fields import CountryField



class CreateOrder(APIView):
    permission_classes = [AllowAny]

    def make_queue_identity(self, request, email: str | None = None) -> Q:
        if request.user.is_authenticated:
            return models.Q(user=request.user)

        guest_token = request.COOKIES.get('guest_token')
        identity_q = Q(guest_token=guest_token) if guest_token else Q(pk__in=[])

        if email:
            identity_q |= Q(user__isnull=True, email=email)

        return identity_q


    def post(self, request):
        if not request.user.has_perm('order.create_order'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            email = request.data.get('email')
            shipping_street = request.data.get('street')
            street_zipcode = request.data.get('zipcode')
            shipping_municipality = request.data.get('municipality')
            shipping_country = request.data.get('country')
            cart = request.data.get('cart')

            if not email or not shipping_street or not street_zipcode or not shipping_municipality or not shipping_country or not cart:
                return Response(
                    {
                        'message': "Your request is incomplete",
                        'email': email,
                        'shipping_street': shipping_street,
                        'street_zipcode': street_zipcode,
                        'shipping_municipality': shipping_municipality,
                        'shipping_country': shipping_country,
                        'cart': cart,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if len(shipping_country) != 2 or not pycountry.countries.get(alpha_2=shipping_country.upper()):
                    return Response(
                        {
                            'message': 'You provided an invalid country code in the sense of ISO 3166-1 alpha-2',
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    serializer = CreateOrderSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)

                    cart = serializer.validated_data['cart']
                    cart_digest = cart_hash(cart)

                    try:
                        minutes = int(os.getenv("CART_DELTA_MINUTES", "30"))
                    except ValueError:
                        minutes = 30

                    duplication_cutoff = timezone.now() - timedelta(minutes=minutes)

                    candidate_duplicate = Order.objects.filter(
                        self.make_queue_identity(request, email),
                        cart_hash=cart_digest,
                        created_at__gte=duplication_cutoff,
                        status__in=[OrderStatus.requires_confirmation, OrderStatus.action_required],
                    ).first()

                    if not candidate_duplicate:
                        # @TODO: Let's copy cart items to OrderedItem and create a new order
                        print("")
                    else:
                        # At this point I expect items to already have been cloned, no further action required.
                        print("")
                        return Response(
                            {
                                'message': 'Order was already created',
                            },
                            status=status.HTTP_200_OK
                        )





