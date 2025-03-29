from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .cart import Cart
from market.models import Product
from .serializers import CartSerializer


class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        cart = Cart(request)
        data = list(cart)
        total_price = cart.get_total_price()

        response_data = {
            "items": data,
            "total_price": total_price
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request):
        cart = Cart(request)
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.add_to_cart(cart)
            return Response(item, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='decrease')
    def decrease(self, request):
        cart = Cart(request)
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.decrease_quantity(cart)
            return Response(item, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'], url_path='remove')
    def remove(self, request):
        cart = Cart(request)
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.remove_from_cart(cart)
            return Response(message, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'], url_path='clear')
    def clear(self, request):
        cart = Cart(request)
        message = {"message": "Cart cleared"}
        cart.clear()
        return Response(message, status=status.HTTP_200_OK)