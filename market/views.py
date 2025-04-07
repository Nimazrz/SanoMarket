from .filters import ProductFilter
from .models import *
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .serializers import ProductSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = '__all__'

# class Product

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
