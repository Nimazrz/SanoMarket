from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

app_name = 'orders'
urlpatterns = [
    path('', include(router.urls)),
]