from django.contrib import admin
from .models import *


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class ProductInfoInline(admin.StackedInline):
    model = ProductInfo
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'offer', 'offer_price', 'offer_start', 'offer_end', 'inventory',
                    'sold_count')
    inlines = [ProductInfoInline, ImageInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'title')
