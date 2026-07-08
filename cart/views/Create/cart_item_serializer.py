from rest_framework import serializers
from catalog.models import ProductVariant

class CartItemSerializer(serializers.Serializer):
    barcode = serializers.SlugRelatedField(
        slug_field="barcode",
        queryset=ProductVariant.objects.all()
    )
    amount = serializers.IntegerField(min_value=0)

