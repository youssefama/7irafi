### shop/models.py
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Artisan(models.Model):
    name = models.CharField(max_length=150)
    biography = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    workshop_photos = models.ManyToManyField('ArtisanPhoto', blank=True)

    def __str__(self):
        return self.name


class ArtisanPhoto(models.Model):
    image = models.ImageField(upload_to='artisans/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Photo {self.id} of artisan"


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    materials = models.CharField(max_length=200)
    dimensions = models.CharField(max_length=100)
    cultural_significance = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='products')
    artisan = models.ForeignKey(Artisan, on_delete=models.SET_NULL, null=True, related_name='products')

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image {self.order} for {self.product.name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} at {self.submitted_at}"