from rest_framework import serializers
from market.models import Product
from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'price', 'quantity', 'get_cost']
        read_only_fields = ['get_cost', 'order']

    def get_cost(self, obj):
        return obj.get_cost()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'buyer', 'address', 'first_name', 'last_name', 'phone',
            'created', 'updated', 'paid', 'items', 'total_cost'
        ]
        read_only_fields = ['created', 'updated', 'total_cost']

    def get_total_cost(self, obj):
        return obj.get_total_cost()

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        for item_data in items_data:
            if 'price' in item_data and item_data['price']:
                raise serializers.ValidationError({"error": "You should not enter price!"})
        order = Order.objects.create(**validated_data)
        order_items = []
        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product'].id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({"error": f"Product with id {item_data['product']} does not exist!"})
            item_price = product.offer_price if product.offer else product.price
            order_items.append(OrderItem(order=order, price=item_price, **item_data))
        OrderItem.objects.bulk_create(order_items)
        return order

    def destroy(self, instance):
        request = self.context['request']
        if request.user.is_authenticated:
            if instance.buyer == request.user:
                instance.delete()
                return instance
            else:
                raise serializers.ValidationError({"error": "You are not authorized to delete this order."})
        else:
            raise serializers.ValidationError({"error": "You are not authorized to delete this order."})
