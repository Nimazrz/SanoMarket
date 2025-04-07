from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet, basename='comments')
router.register(r'products', views.ProductListView, basename='products')


app_name = 'market'

urlpatterns = [
    path('', include(router.urls)),
]