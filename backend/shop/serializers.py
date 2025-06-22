### shop/serializers.py
from rest_framework import serializers
from .models import (Category, Region, Artisan, ArtisanPhoto,
                     Product, ProductImage, ContactMessage)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order']


class ArtisanPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanPhoto
        fields = ['id', 'image', 'caption']


class ArtisanSerializer(serializers.ModelSerializer):
    workshop_photos = ArtisanPhotoSerializer(many=True, read_only=True)
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Artisan
        fields = ['id', 'name', 'biography', 'region', 'workshop_photos', 'products']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    artisan = ArtisanSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'materials', 'dimensions',
            'cultural_significance', 'category', 'region', 'artisan', 'images'
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'submitted_at']
        read_only_fields = ['submitted_at']