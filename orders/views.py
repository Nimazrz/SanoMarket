from rest_framework import viewsets
from orders.models import Order
from orders.serializers import OrderSerializer
import json
import requests
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from market.models import Product
from .models import Order, OrderItem


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(buyer=user)
        return Order.objects.none()


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
CallbackURL = 'http://127.0.0.1:8000/api/payment/verify/'  # آدرس جدید برای DRF


class PaymentRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ایجاد درخواست پرداخت"""
        order_id = request.data.get("order_id")
        try:
            order = Order.objects.get(id=order_id, buyer=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        description = ', '.join([item.product.name for item in order.items.all()])
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_cost(),
            "Description": description,
            "Phone": request.user.phone,
            "CallbackURL": CallbackURL
        }

        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        try:
            response = requests.post(ZP_API_REQUEST, data=json.dumps(data), headers=headers, timeout=10)
            if response.status_code == 200:
                response_json = response.json()
                authority = response_json.get('Authority')
                if response_json.get('Status') == 100:
                    return Response({"startpay_url": ZP_API_STARTPAY + authority}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Payment request failed"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "ZarinPal response failed"}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """تایید پرداخت"""
        order_id = request.query_params.get("order_id")
        authority = request.query_params.get("Authority")

        try:
            order = Order.objects.get(id=order_id, buyer=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_cost(),
            "Authority": authority,
        }

        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        try:
            response = requests.post(ZP_API_VERIFY, data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                response_json = response.json()
                if response_json.get('Status') == 100:
                    order.paid = True
                    order.save()
                    for item in order.items.all():
                        item.product.inventory -= item.quantity
                        item.product.save()
                    return Response({"message": "Payment successful", "RefID": response_json.get('RefID')},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "ZarinPal response failed"}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
