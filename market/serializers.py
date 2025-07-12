from django.http import JsonResponse
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import *


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ['title', 'text']


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['product', 'image_url', 'title', 'description']
        read_only_fields = ['product']

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image_file.url) if obj.image_file else None


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
            if request.user.is_seller:
                info_data = validated_data.pop('info', [])
                image_data = validated_data.pop('images', [])
                validated_data['owner'] = request.user
                product = Product.objects.create(**validated_data)
                if info_data:
                    for info in info_data:
                        ProductInfo.objects.create(product=product, **info)
                if image_data:
                    for image in image_data:
                        Image.objects.create(product=product, **image)
                return product
            else:
                raise serializers.ValidationError({'error': 'You are not seller!'})
        raise serializers.ValidationError({'error': 'You are not Authenticated!'})

    def update(self, instance, validated_data):
        request = self.context.get('request')
        info_data = validated_data.pop('info', [])
        image_data = validated_data.pop('images', [])
        owner = instance.owner
        if request.user.is_authenticated:
            if request.user == owner:
                if request.user.is_seller:
                    for attr, value in validated_data.items():
                        setattr(instance, attr, value)
                    instance.save()
                    instance.info.all().delete()
                    for item in info_data:
                        ProductInfo.objects.create(product=instance, **item)
                    for image in image_data:
                        Image.objects.create(product=instance, **image)
                    return instance
                raise serializers.ValidationError({'error': 'You are not seller!'})
            raise serializers.ValidationError({'error': 'You are not owner of this product!'})
        raise serializers.ValidationError({'error': 'You are not Authenticated!'})

    def destroy(self, instance):
        request = self.context.get('request')
        owner = instance.owner
        if request.user.is_authenticated:
            if request.user == owner:
                if request.user.is_seller:
                    instance.delete()
                    return instance
                raise serializers.ValidationError({"error": "You are not seller!"})
            raise serializers.ValidationError({"error": "You are not owner of this product!"})
        raise serializers.ValidationError({'error': 'You are not Authenticated!'})