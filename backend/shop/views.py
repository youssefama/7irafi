### shop/views.py
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import (Category, Region, Artisan, Product, ContactMessage)
from .serializers import (
    CategorySerializer, RegionSerializer,
    ArtisanSerializer, ProductSerializer,
    ContactMessageSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class ArtisanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artisan.objects.select_related('region').prefetch_related('workshop_photos', 'products')
    serializer_class = ArtisanSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('category', 'region', 'artisan').prefetch_related('images')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category__id', 'region__id']
    search_fields = ['name', 'description', 'materials', 'cultural_significance']


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)