from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from catalog.models import Product

class SoftDeleteProductViewSerializer(serializers.Serializer):
    product = serializers.SlugRelatedField(
        slug_field='product',
        queryset=Product.objects.all()
    )

    schedule = serializers.DateTimeField(allow_null=True)


class SoftDeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            if not request.user.has_perm('catalog.delete_product'):
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = SoftDeleteProductViewSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                product_data = serializer.validated_data
                time_of_deletion = product_data['timeOfDeletion']
                product: Product = product_data['product']

                product.timeOfDeletion = time_of_deletion if time_of_deletion is not None else timezone.now()
                product.save()

                return Response(status=status.HTTP_200_OK)