from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from payment.models import CardPayment
from django.db import IntegrityError


class CreateCardPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            network = request.data.get('network')
            last_4_digits = request.data.get('last_4_digits')
            expiry_date = request.data.get('expiry_date')
            card_owner_name = request.data.get('card_owner_name')

            try:
                payment, did_create = CardPayment.objects.get_or_create(
                    network=network,
                    last_4_digits=last_4_digits,
                    expiry_date=expiry_date,
                    card_owner_name=card_owner_name,
                )

                return Response({
                    'payment_method_id': payment.id,
                }, status=status.HTTP_204_NO_CONTENT if not did_create else status.HTTP_201_CREATED)

            except IntegrityError:
                return Response(
                    {
                        'detail': 'Failed to create payment method because of constraint violation.',
                    }, status=status.HTTP_400_BAD_REQUEST)




