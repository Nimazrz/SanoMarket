from django.db import models
from market.models import Product
from account.models import CustomUser, Address


class Order(models.Model):
    class Status(models.TextChoices):
        AWAITING_PAYMENT = 'awaiting_payment', 'در انتظار پرداخت'
        PAID = 'paid', 'پرداخت شده'
        SHIPPING = 'shipping', 'در حال ارسال'
        DELIVERED = 'delivered', 'تحویل داده شده'
        CANCELLED = 'cancelled', 'لغو شده'
        RETURNED = 'returned', 'مرجوع شده'
    buyer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='orders', null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='orders', null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=Status.choices, default=Status.AWAITING_PAYMENT)
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f"order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1, )

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.offer_price if (self.product.offer_price !=0) else self.product.price
        super().save(*args, **kwargs)

    def get_cost(self):
        return self.price * self.quantity
