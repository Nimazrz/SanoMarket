from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet, basename='comments')
router.register(r'products', views.ProductListView, basename='products')


app_name = 'market'

urlpatterns = [
    path('related_products/<int:product_id>', views.RelatedProductListView.as_view(), name='related_products'),
    path('rate_product/', views.ProductRatingView.as_view(), name='rate_product'),

    path("categories/", views.CategoryListAPIView.as_view()),

    path('', include(router.urls)),
]