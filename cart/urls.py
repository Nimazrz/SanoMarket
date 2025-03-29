from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('cart', views.CartViewSet, basename='cart')

app_name = 'cart'
urlpatterns = [
    path('', include(router.urls)),

]