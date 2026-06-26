import logging
from django.db.models import F
from celery import shared_task
from order.utils.CartHash import CartItem
from order.models import Order, OrderStatus
from catalog.models import ProductVariant

logger = logging.getLogger(__name__)


@shared_task
def reset_stale_cart_stock(cart_hash: str, cart: list[CartItem]):

    try:
        matching_order = Order.objects.get(cart_hash=cart_hash)

        if matching_order.status in [OrderStatus.action_required, OrderStatus.requires_confirmation]:
            products = ProductVariant.objects.filter(
                barcode__in={ cart_item["product"] for cart_item in cart}
            )

            barcode_to_product_map = { product.barcode : product for product in products }

            for cart_item in cart:
                product_barcode_for_this_item = cart_item["product"]
                product_for_this_barcode = barcode_to_product_map.get(product_barcode_for_this_item)

                if not product_for_this_barcode:
                    logger.warning(f"Skipping reset for product with barcode {product_barcode_for_this_item} because no such product was found.")
                else:
                    ProductVariant.objects.filter(barcode=product_barcode_for_this_item).update(
                        stock=F("stock") + cart_item["order_amount"]
                    )

                    logger.info(f"Product {product_for_this_barcode} successfully restored.")
        else:
            logger.info(f"{cart_hash} doesn't need cleanup at least yet.")

    except Order.DoesNotExist:
        logger.error(f"Order {cart_hash} not found. Skipping.")
        pass

    except Order.MultipleObjectsReturned:
        logger.error(f"Multiple orders with hash {cart_hash} found. This is a serious integrity issue as cart_hash is expected to be unique.")
        pass
