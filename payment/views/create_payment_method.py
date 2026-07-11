from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers
from payment.models import PaymentMethod, PaymentMethodTypes
from django.db import IntegrityError

class CreateCardPaymentSerializer(serializers.Serializer):
    network = serializers.CharField(max_length=50)
    last_4_digits = serializers.CharField(max_length=4)
    expiry_date = serializers.DateField( input_formats=["%Y-%m-%d"] )
    card_owner_name = serializers.CharField(max_length=255)

    def validate_last_4_digits(self, value):
        if not value.isdigit() or len(value) != 4:
            raise serializers.ValidationError( "last_4_digits must consist of exactly 4 digits." )

        return value

class CreatePaymentMethod(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            if not request.user.has_perm('payment.add_paymentmethod'):
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = CreateCardPaymentSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                validated_data = serializer.validated_data

                type = validated_data['type']
                name = validated_data['name']
                provider = validated_data['provider']

                if type not in PaymentMethodTypes:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    try:
                        payment, did_create = PaymentMethod.objects.get_or_create(
                            type=type,
                            name=name,
                            provider=provider,
                        )

                        return Response({
                            'payment_method_id': payment.id,
                        }, status=status.HTTP_204_NO_CONTENT if not did_create else status.HTTP_201_CREATED)

                    except IntegrityError:
                        return Response(
                            {
                                'detail': 'Failed to create payment method because of constraint violation.',
                            }, status=status.HTTP_400_BAD_REQUEST)




