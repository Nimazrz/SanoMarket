from rest_framework import serializers

from .models import *

class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ['title', 'text']


class ProductSerializer(serializers.ModelSerializer):
    info = ProductInfoSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'offer', 'offer_price', 'description', 'inventory', 'info']

