from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from order.models import Order
from django.conf import settings
from .create_order_from_cart import CreateOrderFromCartSerializer

class UpdateOrder(APIView):
    permission_classes = [AllowAny]

    def perform_authentication(self, request):
        try:
            super().perform_authentication(request)
        except AuthenticationFailed:
            request._user = AnonymousUser()

    def put(self, request, *args, **kwargs):
        order_id = request.COOKIES.get('order')
        serializer = CreateOrderFromCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        if order_id is not None:
            serializer = CreateOrderFromCartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            validated_data = serializer.validated_data
            order = Order.objects.get(id=order_id)
            self.perform_update(order, validated_data)

            return Response(status=status.HTTP_200_OK)
        else:
            if request.user.is_authenticated:
                try:
                    order = Order.objects.get(user=request.user)
                    self.perform_update(order, validated_data)

                    response = Response(status=status.HTTP_200_OK)

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
                except Order.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)


    def perform_update(self, order: Order, validated_data):
        with transaction.atomic():
            order.email = validated_data['email']
            order.shipping_street = validated_data['shipping_street']
            order.zipcode = validated_data['street_zipcode']
            order.shipping_municipality = validated_data['shipping_municipality']
            order.shipping_country = validated_data['shipping_country']
            order.save()

    post = put
