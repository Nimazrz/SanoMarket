from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from account.models import Address
from .cart import Cart
from orders.models import Order, OrderItem
from market.models import Product
from .serializers import CartSerializer
from django.db import transaction
from django.shortcuts import get_object_or_404


# from .models import Cart as CartModel


class CartViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        cart = Cart(request)
        data = list(cart)
        total_price = cart.get_total_price()

        response_data = {
            "items": data,
            "total_price": total_price
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='decrease', permission_classes=[AllowAny])
    def decrease_item(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = Cart(request)
        response = serializer.remove_from_cart(cart)

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='add', permission_classes=[AllowAny])
    def add_to_cart(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product_id = request.data['product_id']
            product = Product.objects.get(id=product_id)
            cart = Cart(request)
            current_quantity = cart.cart.get(str(product_id), {}).get("quantity", 0)
            if current_quantity >= product.inventory:
                return Response(
                    {"message": "به سقف موجودی محصول رسیده‌اید"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            item = serializer.add_to_cart(cart)
            return Response(item, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='create-order', permission_classes=[AllowAny])
    @transaction.atomic
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

    @action(detail=False, methods=['post'], url_path='decrease', permission_classes=[AllowAny])
    def decrease_item(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = Cart(request)
        response = serializer.decrease_quantity(cart)

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='remove-item', permission_classes=[AllowAny])
    def remove_item(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = Cart(request)
        response = serializer.remove_from_cart(cart)

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='clear', permission_classes=[AllowAny])
    def clear_cart(self, request):
        cart = Cart(request)
        cart.clear()
        return Response({"message": "سبد خرید با موفقیت خالی شد"}, status=status.HTTP_200_OK)
#
# # cart for authenticated users
#
# class CartAuthenticatedUserViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#
#     def list(self, request):
#         cart, _ = CartModel.objects.get_or_create(user=request.user)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)
#
#     @action(detail=False, methods=['post'], url_path='add')
#     def add_product(self, request):
#         product_id = request.data.get('product_id')
#         quantity = request.data.get('quantity', 1)
#
#         try:
#             quantity = int(quantity)
#             if quantity < 1:
#                 raise ValueError
#         except (ValueError, TypeError):
#             return Response({'error': 'تعداد محصول نامعتبر است'}, status=400)
#
#         if not product_id:
#             return Response({'error': 'شناسه محصول لازم است'}, status=400)
#
#         product = get_object_or_404(Product, id=product_id)
#         cart, _ = CartModel.objects.get_or_create(user=request.user)
#
#         try:
#             cart.add_product(product, quantity)
#             return Response({'detail': 'محصول به سبد اضافه شد'})
#         except ValueError as e:
#             return Response({'error': str(e)}, status=400)
#
#     @action(detail=False, methods=['post'], url_path='decrease')
#     def decrease_product(self, request):
#         product_id = request.data.get('product_id')
#         quantity = request.data.get('quantity', 1)
#
#         try:
#             quantity = int(quantity)
#             if quantity < 1:
#                 raise ValueError
#         except (ValueError, TypeError):
#             return Response({'error': 'تعداد نامعتبر'}, status=400)
#
#         if not product_id:
#             return Response({'error': 'شناسه محصول لازم است'}, status=400)
#
#         product = get_object_or_404(Product, id=product_id)
#         cart = get_object_or_404(CartModel, user=request.user)
#         cart.decrease_product(product, quantity)
#         return Response({'detail': 'تعداد محصول کاهش یافت'})
#
#     @action(detail=False, methods=['delete'], url_path='remove')
#     def remove_product(self, request):
#         product_id = request.data.get('product_id')
#         if not product_id:
#             return Response({'error': 'شناسه محصول لازم است'}, status=400)
#
#         product = get_object_or_404(Product, id=product_id)
#         cart = get_object_or_404(CartModel, user=request.user)
#         cart.remove_product(product)
#         return Response({'detail': 'محصول حذف شد'})
