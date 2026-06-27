from typing import TypedDict
from catalog.models import ProductVariant
import hashlib

class CartItem(TypedDict):
    product: ProductVariant
    amount_ordered: int

class SerializableCartItem(TypedDict):
    product_barcode: str
    amount_ordered: int

def cart_hash(cart: list[CartItem]) -> str:
    if not all('product' in item and 'amount_ordered' in item for item in cart):
        raise ValueError('Cart must consist of (product, amount_ordered) tuples')

    sorted_cart = sorted(cart, key=lambda item: item['product'].barcode)
    parts = [f"{item['product'].barcode}:{item['amount_ordered']}" for item in sorted_cart]
    serialized = '|'.join(parts)

    return hashlib.sha256(serialized.encode()).hexdigest()
