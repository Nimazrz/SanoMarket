from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
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

    @action(detail=False, methods=['POST'], url_path='create-order')
    def create_order(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():  # ✅ تراکنش برای جلوگیری از ذخیره ناقص داده‌ها
            order = Order.objects.create(user=request.user, total_price=cart.get_total_price())

            for item in cart:
                product = Product.objects.get(id=item['product']['id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price']
                )

            cart.clear()  # ✅ پاک کردن سبد خرید بعد از ثبت سفارش

        return Response({"message": "Order created successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)