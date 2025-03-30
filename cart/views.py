from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from account.models import Address
from .cart import Cart
from orders.models import Order, OrderItem
from market.models import Product
from .serializers import CartSerializer
from django.db import transaction


class CartViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        cart = Cart(request)
        data = list(cart)
        total_price = cart.get_total_price()

        response_data = {
            "items": data,
            "total_price": total_price
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='create-order', permission_classes=[IsAuthenticated])
    def create_order(self, request):
        """
        data for resaver
        {
            "first_name": "Ali",
            "last_name": "Rezaei",
            "phone": "09123456789",
            "address_id": 1
        }
        """
        user = request.user
        if not user or not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        cart = Cart(request)
        data = cart.cart
        total_price = cart.get_total_price()

        first_name = request.data.get('first_name', user.first_name)
        last_name = request.data.get('last_name', user.last_name)
        phone = request.data.get('phone', user.phone)
        address_id = request.data.get('address_id')

        try:
            address = Address.objects.get(id=address_id, custom_user=user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            buyer=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            total_price=total_price
        )

        for product_id, item in data.items():
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": f"Product with id {product_id} not found"},
                                status=status.HTTP_400_BAD_REQUEST)

            OrderItem.objects.create(
                order=order,
                product=product,
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()

        return Response({"message": "Order created successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)