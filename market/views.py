from .filters import ProductFilter
from .models import *
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .permissions import *
from rest_framework import generics
from django.db.models import Case, When, F, Avg


class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['ordering_price', 'sold_count', 'average_rating']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(
            average_rating=Avg('ratings__stars'),
            ordering_price=Case(
                When(offer_price__isnull=False, then=F('offer_price')),
                default=F('price')
            )
        )
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductRatingView(generics.CreateAPIView):
    serializer_class = ProductRatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RelatedProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = RelatedProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Product.objects.none()
        return Product.objects.filter(category=product.category).exclude(id=product.id)[:10]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = [
            {"key": key, "label": label}
            for key, label in Product.Category.choices
        ]
        return Response(categories)

