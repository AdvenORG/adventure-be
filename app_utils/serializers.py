from rest_framework import serializers

from images.models import Image
from store.models import Category, Product


class SuccessSerializer(serializers.Serializer):
    status_code = serializers.IntegerField(default=200)
    message = serializers.CharField(default="Success")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image", "description", "uploaded_at")
        read_only_fields = ("id", "uploaded_at")


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name="get_images")

    class Meta:
        model = Product
        fields = (
            "product_id",
            "SKU",
            "slug",
            "description",
            "price",
            "stock",
            "images",  # Include the images field in the serializer
            "category",
        )

    def create(self, validated_data):
        print(validated_data)
        return Product.objects.create(**validated_data)

    def get_images(self, obj):
        images = Image.objects.for_model(obj)
        try:
            cache = []
            for obj in images:
                cache += [f"http://127.0.0.1:8000{obj.image.url}"]
            return cache
        except Exception as e:
            raise e


class SuccessProductSerializer(SuccessSerializer):
    data = serializers.SerializerMethodField("get_results")

    def get_results(self, obj):
        serialized_data = ProductSerializer(Product.objects.all(), many=True).data
        return serialized_data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
