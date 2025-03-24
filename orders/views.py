from rest_framework import viewsets
from orders.models import Order
from orders.serializers import OrderSerializer
from django.shortcuts import get_object_or_404


class OrderListCreateView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        orders = Order.objects.filter(buyer=self.request.user)
        return orders

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)