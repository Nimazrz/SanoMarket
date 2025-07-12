from django.db import models
from account.models import CustomUser


class Product(models.Model):
    class Category(models.TextChoices):
        ELECTRONICS = "electronics", "کالای دیجیتال"
        CLOTHING = "clothing", "پوشاک"
        BOOKS = "books", "کتاب و لوازم تحریر"
        HOME_APPLIANCES = "home_appliances", "لوازم خانگی"
        BEAUTY = "beauty", "آرایشی و بهداشتی"
        TOYS = "toys", "اسباب‌بازی و کودک"
        SPORTS = "sports", "ورزشی و سفر"
        FOOD = "food", "خواروبار"
        AUTOMOTIVE = "automotive", "خودرو و موتور"
        JEWELRY = "jewelry", "زیورآلات و اکسسوری"
        FURNITURE = "furniture", "مبلمان و دکوراسیون"
        MEDICAL = "medical", "تجهیزات پزشکی"
        MUSIC = "music", "موسیقی و آلات موسیقی"
        OTHERS = "others", "چیز های دیگر"

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.ELECTRONICS,
        db_index=True
    )
    price = models.PositiveIntegerField(default=0)
    offer = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    offer_price = models.PositiveIntegerField(null=True, blank=True)
    inventory = models.PositiveIntegerField(default=0, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        ordering = ['created_at']


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='info')
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product_info'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=255)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to=f'{product.name}/', max_length=500, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else self.image_file

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
