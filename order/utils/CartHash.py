from typing import TypedDict
from catalog.models import ProductVariant
import hashlib

class CartItem(TypedDict):
    product: ProductVariant
    order_amount: int


def cart_hash(cart: list[CartItem]) -> str:
    if not all('product' in item and 'order_amount' in item for item in cart):
        raise ValueError('Cart must consist of (product, order_amount) tuples')

    sorted_cart = sorted(cart, key=lambda item: item['product'].barcode)
    parts = [f"{item['product'].barcode}:{item['order_amount']}" for item in sorted_cart]
    serialized = '|'.join(parts)

    return hashlib.sha256(serialized.encode()).hexdigest()
