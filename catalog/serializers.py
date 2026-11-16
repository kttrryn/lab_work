from rest_framework import serializers

from .models import Brand, Category, Product, ProductVariation


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "description"]


class SubCategorySerializer(
    serializers.ModelSerializer
):  # для елементів всередині поля subcategories
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryTreeSerializer(serializers.ModelSerializer):  # для випадаючого меню
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "subcategories"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent"]


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ["id", "color_name", "stock_quantity"]


class ProductListSerializer(serializers.ModelSerializer):  # /api/v1/products
    brand = serializers.CharField(source="brand.name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "brand"]


class ProductDetailSerializer(serializers.ModelSerializer):  # /api/v1/products/{id}
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), source="brand", write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    available_colors = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "description",
            "price",
            "brand",
            "brand_id",
            "category_id",
            "available_colors",
        ]

    def get_available_colors(self, obj):
        return list(obj.variations.values_list("color_name", flat=True))
