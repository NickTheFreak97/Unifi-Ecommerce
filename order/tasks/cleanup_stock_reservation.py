import logging
from django.db.models import Q, F
from celery import shared_task
from order.utils.CartHash import SerializableCartItem
from order.models import Order, OrderedItem, OrderStatus
from catalog.models import ProductVariant
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def reset_stale_cart_stock(order_id: str, cart: list[SerializableCartItem]):

    try:
        matching_order = Order.objects.get(id=order_id)

        if matching_order.status in { OrderStatus.action_required, OrderStatus.requires_confirmation }:
            products = ProductVariant.objects.filter(
                barcode__in={cart_item["product_barcode"] for cart_item in cart}
            ).filter(
                Q(product__timeOfDeletion__isnull=True) | Q(product__timeOfDeletion__gt=timezone.now())
            )

            barcode_to_product_map = { product.barcode : product for product in products }

            with transaction.atomic():
                for cart_item in cart:
                    product_barcode_for_this_item = cart_item["product_barcode"]
                    product_for_this_barcode = barcode_to_product_map.get(product_barcode_for_this_item)

                    if not product_for_this_barcode:
                        logger.warning(f"Skipping reset for product with barcode {product_barcode_for_this_item} because no such product was found.")
                    else:
                        ProductVariant.objects.filter(barcode=product_barcode_for_this_item).update(
                            stock=F("stock") + cart_item["amount_ordered"]
                        )

                        logger.info(f"Product {product_for_this_barcode} successfully restored.")

                OrderedItem.objects.filter(order=matching_order).delete()
                matching_order.delete()

            # TODO: Cleanup payment intent
        else:
            logger.info(f"{order_id} doesn't need cleanup at least yet.")

    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found. Skipping.")
        pass

    except Order.MultipleObjectsReturned:
        logger.error(f"Multiple orders with id {order_id} found. This is a serious integrity issue as cart_hash is expected to be unique.")
        pass