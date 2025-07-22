from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from orders.models import Order, OrderItem


# @receiver(pre_save, sender=OrderItem)
# def add_price(sender, instance, **kwargs):
#     product_price = instance.product.offer_price if instance.product.offer_price > 0 else instance.product.price
#     instance.price = product_price
#     instance.save()


@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total_price(sender, instance, **kwargs):
    order = instance.order
    total = sum(item.get_cost() for item in order.items.all())
    order.total_price = total
    order.save(update_fields=['total_price'])