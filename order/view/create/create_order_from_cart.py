from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django_redis import get_redis_connection
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from django.conf import settings
import pycountry
from order.models import Order
from order.view.create.create_order import clone_products_to_order_items, decrease_stock_for_ordered_items, schedule_refill_stock_for_stale_orders, CartItem
from .create_order import cart_hash

from cart.models import Cart
from catalog.models import ProductVariant


class CreateOrderFromCartSerializer(serializers.Serializer):
    email = serializers.EmailField()
    street = serializers.CharField(source='shipping_street')
    zipcode = serializers.CharField(source='street_zipcode')
    municipality = serializers.CharField(source='shipping_municipality')
    country = serializers.CharField(source='shipping_country')
    currency = serializers.CharField()

    def validate_currency(self, currency):
        if pycountry.currencies.get(alpha_3=currency.upper()) is None:
            raise serializers.ValidationError('Invalid currency code in the sense of ISO 4217.')
        else:
            return currency

    def validate_country(self, candidate_country_code):
        if len(candidate_country_code) != 2 or not pycountry.countries.get(alpha_2=candidate_country_code.upper()):
            raise serializers.ValidationError(
                "Invalid ISO 3166-1 alpha-2 country code."
            )
        return candidate_country_code.upper()


class CreateOrderFromCart(APIView):
    permission_classes = [AllowAny]

    def perform_authentication(self, request):
        try:
            super().perform_authentication(request)
        except AuthenticationFailed:
            request._user = AnonymousUser()

    def post(self, request):
        if request.user.is_authenticated and not request.user.has_perm('order.create_order'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            if request.COOKIES.get('order') is not None:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:

                serializer = CreateOrderFromCartSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                order_data = serializer.validated_data

                email = order_data['email']
                shipping_street = order_data['shipping_street']
                street_zipcode = order_data['street_zipcode']
                shipping_municipality = order_data['shipping_municipality']
                shipping_country = order_data['shipping_country']

                if not email or not shipping_street or not street_zipcode or not shipping_municipality or not shipping_country:
                    return Response(
                        {
                            'message': "Your request is incomplete",
                            'email': email,
                            'shipping_street': shipping_street,
                            'street_zipcode': street_zipcode,
                            'shipping_municipality': shipping_municipality,
                            'shipping_country': shipping_country,
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    cart: list[CartItem] = []

                    if request.user.is_authenticated:
                        cart_for_this_user = Cart.objects.select_related('product').filter(user=request.user)

                        if not cart_for_this_user.exists():
                            return Response(status=status.HTTP_404_NOT_FOUND)
                        else:
                            cart = [
                                    CartItem(
                                        product=cart_item.product,
                                        quantity=cart_item.quantity
                                    )
                                    for cart_item in cart_for_this_user
                                ]
                    else:
                        guest_token = request.COOKIES.get('guest_token')

                        if guest_token is not None:
                            redis = get_redis_connection('default')
                            user_cart_key = "cart:{user_id}".format(user_id=guest_token)
                            cart_mapping_hash = redis.hgetall(user_cart_key)

                            if cart_mapping_hash:
                                cart_mapping = {
                                    barcode.decode(): quantity
                                    for barcode,quantity in cart_mapping_hash.items()
                                }

                                products_in_cart = ProductVariant.objects.filter(
                                    barcode__in=cart_mapping.keys()
                                )

                                cart = [
                                    CartItem(
                                        product=product,
                                        quantity=cart_mapping[product.barcode]
                                    )
                                    for product in products_in_cart
                                ]
                            else:
                                return Response(status=status.HTTP_404_NOT_FOUND)
                        else:
                            return Response(status=status.HTTP_401_UNAUTHORIZED)

                    if len(cart) <= 0:
                        # If I don't do this, an empty cart causes runtime crash because price sums to 0 and I have a gt=0
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    else:
                        with transaction.atomic():
                            order = Order.objects.create(
                                user=request.user if request.user.is_authenticated else None,
                                email=serializer.validated_data['email'],
                                price=sum(item['product'].unitPrice * item['quantity'] for item in cart),
                                currency=serializer.validated_data['currency'],
                                shipping_street=serializer.validated_data['shipping_street'],
                                street_zipcode=serializer.validated_data['street_zipcode'],
                                shipping_municipality=serializer.validated_data['shipping_municipality'],
                                shipping_country=serializer.validated_data['shipping_country'],
                                cart_hash=cart_hash([
                                    {
                                        "product": cart_item['product'],
                                        "amount_ordered": cart_item['quantity']
                                    }

                                    for cart_item in cart
                                ]),
                                guest_token=request.COOKIES.get('guest_token') if request.COOKIES.get(
                                    'guest_token') and not request.user.is_authenticated else None,
                            )

                            clone_products_to_order_items(
                                order=order,
                                cart=cart,
                                currency=serializer.validated_data['currency']
                            )

                            insufficient = decrease_stock_for_ordered_items(cart=cart)

                            if len(insufficient) > 0:
                                transaction.set_rollback(True)
                                return Response(
                                    {
                                        'message': "Insufficient stock for at least one product",
                                        'insufficient_stock': insufficient,
                                    },
                                    status=status.HTTP_409_CONFLICT
                                )

                            schedule_refill_stock_for_stale_orders(
                                order=order,
                                cart=cart,
                            )
                            response = Response(
                                {
                                    "message": "Order created successfully",
                                    'order': order.id,
                                },
                                status=status.HTTP_200_OK
                            )

                            response.set_cookie(
                                'order',
                                order.id,
                                max_age=60 * 60 * 24 * 7,
                                httponly=True,
                                secure=not settings.DEBUG,
                                samesite="Lax",
                                path="/",
                            )

                            return response