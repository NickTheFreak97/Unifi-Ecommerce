from rest_framework import serializers
from catalog.models import ProductVariant


class OrderCreationSerializer(serializers.Serializer):
    product = serializers.SlugRelatedField(
        slug_field='barcode',
        queryset=ProductVariant.objects.all()
    )
    order_amount = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    cart = OrderCreationSerializer(many=True, allow_empty=False)
