from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Region, Artisan, Product, ContactMessage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Region
        fields = ['id', 'name']


class ArtisanRegistrationSerializer(serializers.ModelSerializer):
    # accept credentials + artisan fields
    username     = serializers.CharField(write_only=True)
    password     = serializers.CharField(write_only=True, min_length=8)
    region_id    = serializers.PrimaryKeyRelatedField(
                       queryset=Region.objects.all(),
                       source='region',
                       write_only=True,
                   )
    main_image   = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model  = Artisan
        fields = ['username','password','name','biography','region_id','main_image']

    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('username'),
        }
        password = validated_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()

        # use the remaining data (name, biography, region, main_image)
        artisan = Artisan.objects.create(user=user, **validated_data)
        return artisan


class ArtisanSerializer(serializers.ModelSerializer):
    # nested read-only region
    region = RegionSerializer(read_only=True)
    # write-only flat field for create/update
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        source='region',
        write_only=True,
        allow_null=True
    )
    # image field is both read & write
    main_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model  = Artisan
        fields = ['id', 'name', 'biography', 'region', 'region_id', 'main_image']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    region   = RegionSerializer(read_only=True)
    artisan  = ArtisanSerializer(read_only=True)

    # write-only flat fields
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    region_id   = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),   source='region',   write_only=True
    )
    artisan_id  = serializers.PrimaryKeyRelatedField(
        queryset=Artisan.objects.all(),  source='artisan',  write_only=True, allow_null=True
    )
    main_image  = serializers.ImageField(required=False, allow_null=True)
    price       = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'description', 'materials', 'dimensions',
            'cultural_significance',
            'category', 'category_id',
            'region',   'region_id',
            'artisan',  'artisan_id',
            'main_image', 'price',
        ]

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'submitted_at']
        read_only_fields = ['submitted_at']