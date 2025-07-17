from rest_framework import serializers
from market.models import Product
from django.shortcuts import get_object_or_404
from .models import *

# cart for unknown users


class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def add_to_cart(self, cart):
        product_id = self.validated_data['product_id']
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)
        return cart.cart[str(product.id)]

    def decrease_quantity(self, cart):
        product_id = self.validated_data['product_id']
        product = get_object_or_404(Product, id=product_id)
        cart.decrease(product)
        return cart.cart.get(str(product_id))

    def remove_from_cart(self, cart):
        product_id = self.validated_data['product_id']
        if str(product_id) not in cart.cart:
            raise serializers.ValidationError({"error": "Product not in cart"})
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return {"message": "Product removed"}

    def clear_cart(self, cart):
        cart.clear()
        return {"message": "Cart cleared"}


class CartItemSerializer(serializers.Serializer):
    product = serializers.CharField(source='product.name', read_only=True)
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        price = obj.get('price', 0)
        quantity = obj.get('quantity', 1)
        return price * quantity

# cart for authenticated users
#
#
# class CartItemAuthenticatedUserSerializer(serializers.ModelSerializer):
#     product_name = serializers.CharField(source='product.name', read_only=True)
#     product_price = serializers.SerializerMethodField()
#     total_price = serializers.SerializerMethodField()
#
#     class Meta:
#         model = CartItem
#         fields = ['id', 'product', 'product_name', 'quantity', 'product_price', 'total_price']
#
#     def get_product_price(self, obj):
#         return obj.unit_price()
#
#     def get_total_price(self, obj):
#         return obj.total_price()
#
#
# class CartAuthenticatedUserSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)
#     total_cost = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'items', 'total_cost']
#
#     def get_total_cost(self, obj):
#         return obj.total_cost()
