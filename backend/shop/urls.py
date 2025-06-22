### shop/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, RegionViewSet,
    ArtisanViewSet, ProductViewSet,
    ContactMessageViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'artisans', ArtisanViewSet, basename='artisan')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'contact', ContactMessageViewSet, basename='contact')

urlpatterns = [
    path('api/', include(router.urls)),
]