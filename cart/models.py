# from django.db import models
# from account.models import CustomUser
# from market.models import Product
#
#
# class Cart(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def add_product(self, product, quantity=1):
#         item, created = CartItem.objects.get_or_create(cart=self, product=product)
#
#         if item.quantity + quantity > product.stock:
#             raise ValueError("Quantity exceeds available stock.")
#
#         item.quantity += quantity
#         item.save()
#         return item
#
#     def decrease_product(self, product, quantity=1):
#         try:
#             item = CartItem.objects.get(cart=self, product=product)
#             item.quantity -= quantity
#             if item.quantity <= 0:
#                 item.delete()
#             else:
#                 item.save()
#         except CartItem.DoesNotExist:
#             pass
#
#     def remove_product(self, product):
#         try:
#             item = CartItem.objects.get(cart=self, product=product)
#             item.delete()
#         except CartItem.DoesNotExist:
#             pass
#
#     def clear_cart(self):
#         self.items.all().delete()
#
#     def total_cost(self):
#         return sum(item.total_price() for item in self.items.all())
#
#     def __str__(self):
#         return f"{str(self.user.get_full_name())}'s cart"
#
#     class Meta:
#         verbose_name = 'Cart'
#         verbose_name_plural = 'Cart'
#
#
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def unit_price(self):
#         return self.product.offer_price if self.product.offer_price else self.product.price
#
#     def total_price(self):
#         return self.unit_price() * self.quantity
#
#     def __str__(self):
#         return f"{self.product.name} x {self.quantity}"
#
#     class Meta:
#         verbose_name = 'CartItem'
#         verbose_name_plural = 'CartItem'
#         constraints = [
#             models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product'),
#         ]
