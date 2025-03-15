from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product


@receiver(pre_save, sender=Product)
def update_offer_price(sender, instance, **kwargs):
    try:
        if instance.price <= 0:
            raise ValueError("Price must be a positive integer.")

        if not instance.offer or instance.offer == 0:
            instance.offer = None
            instance.offer_price = None
        else:
            if instance.offer > 100:
                raise ValueError("Offer percentage cannot be greater than 100.")

            discount_amount = (instance.offer / 100) * instance.price
            instance.offer_price = int(instance.price - discount_amount)

    except Exception as e:
        print(f"Error in update_offer_price signal: {e}")