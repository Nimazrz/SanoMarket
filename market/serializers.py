from django.http import JsonResponse
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import *


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ['title', 'text']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['product', 'image_file', 'title', 'description']
        read_only_fields = ['product']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'title', 'text']
        read_only_fields = ['user', 'product']


class ProductSerializer(serializers.ModelSerializer):
    info = ProductInfoSerializer(many=True)
    images = ImageSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'owner', 'category', 'price', 'offer', 'offer_price', 'description', 'inventory',
                  'info', 'images', 'comments']
        read_only_fields = ['owner', 'comments']
        update_fields = ['info', 'images', 'comments']

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.is_authenticated:
            info_data = validated_data.pop('info', [])
            image_data = validated_data.pop('images', [])
            product = Product.objects.create(owner=request.user, **validated_data)
            for info in info_data:
                ProductInfo.objects.create(product=product, **info)
            for image in image_data:
                Image.objects.create(product=product, **image)
            return product
        else:
            return Response({'error': 'You are not Authenticated!'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        info_data = validated_data.pop('info', [])
        image_data = validated_data.pop('images', [])
        owner = instance.owner
        if request.user.is_authenticated:
            if request.user == owner:
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                instance.info.all().delete()
                for item in info_data:
                    ProductInfo.objects.create(product=instance, **item)
                for image in image_data:
                    Image.objects.create(product=instance, **image)
                return instance
            else:
                return Response({'error': 'You are not owner of this product!'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'You are not Authenticated!'}, status=status.HTTP_403_FORBIDDEN)