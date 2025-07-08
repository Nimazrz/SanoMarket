from rest_framework import serializers
from market.models import Product
from django.shortcuts import get_object_or_404


class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def add_to_cart(self, cart):
        product_id = self.validated_data['product_id']
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)
        return cart.cart[str(product.id)]

    def decrease_quantity(self, cart):
        product_id = self.validated_data['product_id']
        if str(product_id) not in cart.cart:
            raise serializers.ValidationError({"error": "Product not in cart"})
        product = get_object_or_404(Product, id=product_id)
        cart.decrease(product)
        return cart.cart[str(product_id)]

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
