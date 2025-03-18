from django.http import JsonResponse
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
        fields = ['id', 'name', 'owner', 'category', 'price', 'offer', 'offer_price', 'description', 'inventory', 'info']
        read_only_fields = ['owner']

    def create(self, validated_data):
        request = self.context.get('request')
        info_data = validated_data.pop('info', [])
        product = Product.objects.create(owner=request.user, **validated_data)
        for item in info_data:
            ProductInfo.objects.create(product=product, **item)
        return product

    def update(self, instance, validated_data):
        request = self.context.get('request')
        info_data = validated_data.pop('info', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.owner = request.user
        instance.save()
        instance.info.all().delete()
        for item in info_data:
            ProductInfo.objects.create(product=instance, **item)
        return instance
