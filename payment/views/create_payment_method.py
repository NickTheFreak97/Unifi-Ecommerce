from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers
from payment.models import PaymentMethod, PaymentMethodTypes
from django.db import IntegrityError

class CreatePaymentMethodSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=PaymentMethodTypes)
    name = serializers.CharField(required=True)
    provider = serializers.CharField(required=True)


class CreatePaymentMethod(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            if not request.user.has_perm('payment.add_paymentmethod'):
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = CreatePaymentMethodSerializer(data=request.data)
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




