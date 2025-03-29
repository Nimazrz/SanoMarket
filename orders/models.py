from django.db import models
from market.models import Product
from account.models import CustomUser, Address


class Order(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='orders', null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='orders', null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f"order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.PositiveIntegerField(default=0, )
    quantity = models.PositiveIntegerField(default=1, )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
