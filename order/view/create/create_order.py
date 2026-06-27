from datetime import timedelta
from django.db import models, transaction
from django.db.models import Q, F
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import os


from .create_order_serializer import CreateOrderSerializer
from order.utils.CartHash import cart_hash
from order.models import Order, OrderStatus, OrderedItem
from catalog.models import ProductVariant
from order.tasks.cleanup_stock_reservation import reset_stale_cart_stock



# TODO: Could consider letting the client generate an idempotency key and optionally attach it to the request body.
# If the request includes a key, then lookup cart via the provided key, else, use the current flow
# FIXME: If the user quickly POSTs twice (or more) to this endpoint, since there's no lock between duplicate order check and order creation tied to the user's identity,
# you can end up with two+ orders with the same cart_hash associated with the same user, which is an integrity violation and causes except Order.MultipleObjectsReturned on
# cleanup task execution. PostgreSQL allows the creation of advisory locks (related to app semantics) via `pg_advisory_xact_lock`. You can create one to mimic the user
# identity filter, and wrap all the view code in transaction.atomic() from `candidate_duplicate` SELECT onwards. At the beginning of the transaction run:
# `cursor.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", [lock_key])` replacing `lock_key` with a unique string depending on email | guest_token | cart_hash.
# Else, another strategy worth trying is to use Redis as a cache: use `lock_key` as a cache key, and then try to lock before entering the critical section. If locking fails
# you return a response asking the user to retry shortly. Since transaction.atomic() doesn't have callbacks for `onCommit` or `onRollback` and the lock needs to be released anyway,
# we can just add a `finally` block to release it.
class CreateOrder(APIView):
    permission_classes = [AllowAny]

    @classmethod
    def make_queue_identity(cls, request, email: str | None = None) -> Q:
        # FIXME: Two guest users who typed the same email can still collide
        if request.user.is_authenticated:
            return Q(user=request.user)

        guest_token = getattr(request, "guest_token", None) or request.COOKIES.get("guest_token")

        if guest_token:
            return Q(guest_token=guest_token)
        else:
            if email:
                return Q(user__isnull=True, guest_token__isnull=True, email=email)
            else:
                return Q(pk__in=[])

    def post(self, request):
        if request.user.is_authenticated and not request.user.has_perm('order.create_order'):
            return Response(status=status.HTTP_403_FORBIDDEN)
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
                    cart_barcodes_to_ordered_amount_map = { cart_item.get('product').barcode : cart_item.get("order_amount") for cart_item in cart }

                    if not products_for_barcodes:
                        return Response(
                            {
                                'message': "Empty cart",
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    else:
                        with transaction.atomic():
                            order = Order.objects.create(
                                user=request.user if request.user.is_authenticated else None,
                                email=serializer.validated_data['email'],
                                price=0,  # FIXME: Add actual price computed from cart
                                currency=serializer.validated_data['currency'],
                                shipping_street=serializer.validated_data['street'],
                                street_zipcode=serializer.validated_data['zipcode'],
                                shipping_municipality=serializer.validated_data['municipality'],
                                shipping_country=serializer.validated_data['country'],
                                cart_hash=cart_digest,
                                guest_token=request.COOKIES.get('guest_token') if request.COOKIES.get(
                                    'guest_token') and not request.user.is_authenticated else None,
                            )

                            products_to_clone_query = ProductVariant.objects.filter(
                                barcode__in=cart_barcodes_to_ordered_amount_map.keys(),
                            )

                            # TODO: Create a star topology to convert rates in case the request currency is different from that of the product variant instance
                            items_to_create = [
                                OrderedItem(
                                    order=order,
                                    product=product.barcode,
                                    amount_ordered=cart_barcodes_to_ordered_amount_map.get(product.barcode),
                                    unit_price_at_purchase_time=product.unitPrice,
                                    currency=serializer.validated_data['currency']
                                )
                                for product in products_to_clone_query
                            ]

                            OrderedItem.objects.bulk_create(items_to_create)

                            stock_updates: dict[str, int] = {
                                product.barcode: cart_barcodes_to_ordered_amount_map[product.barcode]
                                for product in products_to_clone_query
                            }

                            locked = {
                                p.barcode: p
                                for p in ProductVariant.objects
                                .select_for_update()
                                .filter(barcode__in=stock_updates.keys())
                                .order_by("barcode")
                            }

                            insufficient = [
                                product_barcode for product_barcode, amount_ordered in stock_updates.items()
                                if locked[product_barcode].stock < amount_ordered
                            ]

                            if insufficient:
                                # FIXME: As I just found out, returning from a transaction in Django results in COMMIT. Must raise an exception to ROLLBACK.
                                return Response(
                                    {
                                        'message': "Insufficient stock for at least one product",
                                        'insufficient_stock': insufficient,
                                    },
                                    status=status.HTTP_409_CONFLICT
                                )

                            for product_barcode, amount_ordered in stock_updates.items():
                                ProductVariant.objects.filter(barcode=product_barcode).update(stock=F("stock") - amount_ordered)

                            reset_stale_cart_stock_payload = [
                                {
                                    "product_barcode": product['product'].barcode,
                                    "amount_ordered": product['amount_ordered'],
                                }
                                for product in cart
                            ]

                            reset_stale_cart_stock.apply_async(
                                args = (order.id, reset_stale_cart_stock_payload),
                                countdown = 60 * 15
                            )

                            # TODO: Create and link payment intent for this order
                            return Response(
                                {
                                    "message": "Order created successfully",
                                    'order': order.id,
                                    'cart': cart_digest,
                                },
                                status=status.HTTP_200_OK
                            )


                else:
                    # At this point I expect items to already have been cloned, no further action required.

                    return Response(
                        {
                            'message': 'Order was already created',
                            'order': candidate_duplicate.id
                        },
                        status=status.HTTP_200_OK
                    )