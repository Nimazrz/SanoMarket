from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet, basename='comments')

app_name = 'market'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='products' ),
    path('', include(router.urls)),
]