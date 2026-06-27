from rest_framework import serializers
from catalog.models import ProductVariant
import pycountry


class OrderCreationSerializer(serializers.Serializer):
    product = serializers.SlugRelatedField(
        slug_field='barcode',
        queryset=ProductVariant.objects.all()
    )
    amount_ordered = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    email = serializers.EmailField()
    street = serializers.CharField(source='shipping_street')
    zipcode = serializers.CharField(source='street_zipcode')
    municipality = serializers.CharField(source='shipping_municipality')
    country = serializers.CharField(source='shipping_country')
    cart = OrderCreationSerializer(many=True, allow_empty=False)
    currency = serializers.CharField(source='currency')

    def validate_currency(self, currency):
        if pycountry.currencies.get(alpha_3=currency.upper()) is None:
            raise serializers.ValidationError('Invalid currency code in the sense of ISO 4217.')
        else:
            return currency

    def validate_shipping_country(self, candidate_country_code):
        if len(candidate_country_code) != 2 or not pycountry.countries.get(alpha_2=candidate_country_code.upper()):
            raise serializers.ValidationError(
                "Invalid ISO 3166-1 alpha-2 country code."
            )
        return candidate_country_code.upper()

    def validate_cart(self, candidate_cart):
        barcodes = [cart_item["product"].barcode for cart_item in candidate_cart]

        if not barcodes:
            raise serializers.ValidationError("Empty cart.")
        else:
            if len(barcodes) != len(set(barcodes)):
                raise serializers.ValidationError(
                    "Duplicate products are not allowed. Please group into a single product.")
            else:
                db_products_for_barcodes = ProductVariant.objects.filter(barcode__in=barcodes)
                db_barcode_to_product_map = {product.barcode: product for product in db_products_for_barcodes}

                not_found_set = set(barcodes) - set(db_barcode_to_product_map.keys())
                if not_found_set:
                    raise serializers.ValidationError({
                        "message": "At least one of the specified barcodes doesn't map to a product.",
                        "missing": list(not_found_set)
                    })
                else:
                    product_barcode_to_order_amount_map = {
                        cart_item["product"].barcode: cart_item["amount_ordered"]
                        for cart_item in candidate_cart
                    }

                    insufficient_stock_items = []

                    for product_obj in db_products_for_barcodes:
                        matching_cart_item_requested_amount = product_barcode_to_order_amount_map.get(
                            product_obj.barcode)

                        if product_obj.stock < matching_cart_item_requested_amount:
                            insufficient_stock_items.append(product_obj.barcode)

                    if insufficient_stock_items:
                        raise serializers.ValidationError({
                            'message': "At least one of the specified order requested amounts exceeds availability in stock.",
                            'product_barcode': insufficient_stock_items
                        })

                    return candidate_cart
