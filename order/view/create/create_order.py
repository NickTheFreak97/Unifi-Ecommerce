from datetime import timedelta
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .create_order_serializer import CreateOrderSerializer
from order.utils.CartHash import cart_hash
import os
from order.models import Order, OrderStatus, OrderedItem
from catalog.models import ProductVariant




class CreateOrder(APIView):
    permission_classes = [AllowAny]

    @classmethod
    def make_queue_identity(cls, request, email: str | None = None) -> Q:
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
                    CreateOrder.make_queue_identity(request, email),
                    cart_hash=cart_digest,
                    created_at__gte=duplication_cutoff,
                    status__in=[OrderStatus.requires_confirmation, OrderStatus.action_required],
                ).first()

                if not candidate_duplicate:
                    cart_barcodes = { cart_item.get('product').barcode for cart_item in cart }
                    products_for_barcodes = ProductVariant.objects.filter(barcode__in=cart_barcodes)
                    cart_barcodes_to_ordered_amount_map = { cart_item.get('product').barcode : cart_item.get("ordered_amount") for cart_item in cart }

                    if not products_for_barcodes:
                        return Response(
                            {
                                'message': "Empty cart",
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    else:
                        """
                            id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
                            user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=False, related_name='orders')
                            email = models.EmailField(default=None)
                            status = models.CharField(max_length=21, choices=OrderStatus, default=OrderStatus.requires_confirmation)
                            price = models.DecimalField(max_digits=6, decimal_places=2)
                            currency = models.CharField(max_length=3)
                            shipping_street = models.CharField(max_length=127)
                            street_zipcode = models.CharField(max_length=10)
                            shipping_municipality = models.CharField(max_length=31)
                            shipping_country = models.CharField(max_length=2)
                            time_of_creation = models.DateField(auto_now_add=True)
                            cart_hash = models.CharField(max_length=64, db_index=True, default=None, unique=True)
                            guest_token = models.UUIDField(null=True, blank=True, db_index=True)
                        """
                        order = Order.objects.create(
                            user = request.user if request.user.is_authenticated else None,
                            email = serializer.validated_data['email'],
                            price = 0, # FIXME: Add actual price computed from cart
                            currency = "USD", # FIXME: Replace with validated value from request,
                            shipping_street = serializer.validated_data['street'],
                            street_zipcode = serializer.validated_data['zipcode'],
                            shipping_municipality = serializer.validated_data['municipality'],
                            shipping_country = serializer.validated_data['country'],
                            cart_hash = cart_digest,
                            guest_token = request.COOKIES.get('guest_token') if request.COOKIES.get('guest_token') and not request.user.is_authenticated else None,
                        )

                        with transaction.atomic():
                            items_to_create = [
                                OrderedItem(
                                    order=order,
                                    product=cart_item['product'],
                                    amount_ordered=cart_item['order_amount'],
                                    unit_price_at_purchase_time=cart_item['product'].price,
                                )
                                for cart_item in cart
                            ]

                            OrderedItem.objects.bulk_create(items_to_create)


                else:
                    # At this point I expect items to already have been cloned, no further action required.

                    return Response(
                        {
                            'message': 'Order was already created',
                        },
                        status=status.HTTP_200_OK
                    )