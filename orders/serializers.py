from rest_framework import serializers
from orders.models import Order, OrderItem
from market.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # چون order مربوط به چندین item هست
    total_cost = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)  # اضافه کردن مجموع هزینه

    class Meta:
        model = Order
        fields = [
            'id', 'buyer', 'address', 'first_name', 'last_name',
            'phone', 'postal_code', 'province', 'city',
            'created', 'updated', 'paid', 'items', 'total_cost'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_cost'] = instance.get_total_cost()
        return representation
