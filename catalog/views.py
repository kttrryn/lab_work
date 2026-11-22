import logging
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import OpenApiResponse, extend_schema
from .models import Brand, Category, Product
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    CategoryTreeSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)
from .utils import error_response

logger = logging.getLogger('catalog')


class BrandListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        summary="Список брендів",
        responses={200: BrandSerializer(many=True)},
    )
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Створення нового бренду",
        request=BrandSerializer,
        responses={
            201: BrandSerializer,
            400: OpenApiResponse(description="Помилка валідації даних"),
            401: OpenApiResponse(description="Користувач не авторизований"),
            403: OpenApiResponse(description="Доступ дозволено лише адміністраторам"),
        },
    )
    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            brand = serializer.save()
            logger.info("Користувач %s створив бренд id=%s", request.user.username, brand.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            "Невдала спроба створення бренду користувачем %s: %s",
            request.user.username,
            serializer.errors,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return None

    @extend_schema(
        summary="Деталі бренду",
        responses={
            200: BrandSerializer,
            404: OpenApiResponse(description="Бренд не знайдено"),
        },
    )
    def get(self, request, pk):
        brand = self.get_object(pk)
        if not brand:
            logger.warning("Запит до неіснуючого бренду id=%s", pk)
            return error_response("Brand not found", status.HTTP_404_NOT_FOUND)
        serializer = BrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Оновлення бренду",
        request=BrandSerializer,
        responses={
            200: BrandSerializer,
            400: OpenApiResponse(description="Помилка валідації даних"),
            401: OpenApiResponse(description="Користувач не авторизований"),
            403: OpenApiResponse(description="Доступ дозволено лише адміністраторам"),
            404: OpenApiResponse(description="Бренд не знайдено"),
        },
    )
    def put(self, request, pk):
        brand = self.get_object(pk)
        if not brand:
            logger.warning("Спроба оновити неіснуючий бренд id=%s", pk)
            return error_response("Brand not found", status.HTTP_404_NOT_FOUND)
        serializer = BrandSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Користувач %s оновив бренд id=%s", request.user.username, pk)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning("Помилка валідації при оновленні бренду id=%s: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Видалення бренду",
        responses={
            204: OpenApiResponse(description="Бренд успішно видалено"),
            401: OpenApiResponse(description="Користувач не авторизований"),
            403: OpenApiResponse(description="Доступ дозволено лише адміністраторам"),
            404: OpenApiResponse(description="Бренд не знайдено"),
            409: OpenApiResponse(description="Неможливо видалити бренд із прив'язаними товарами"),
        },
    )
    def delete(self, request, pk):
        brand = self.get_object(pk)
        if not brand:
            logger.warning("Спроба видалити неіснуючий бренд id=%s", pk)
            return error_response("Brand not found", status.HTTP_404_NOT_FOUND)

        count = brand.products.count()
        if count > 0:
            logger.error(
                "Конфлікт при видаленні бренду id=%s користувачем %s: закріплено %s товарів",
                pk,
                request.user.username,
                count,
            )
            return error_response(
                f"Can't delete the brand as it contains {count} products",
                status.HTTP_409_CONFLICT,
            )

        brand.delete()
        logger.info("Користувач %s видалив бренд id=%s", request.user.username, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        # кореневі категорії та підкатегорії
        root_categories = Category.objects.filter(parent=None).prefetch_related(
            "subcategories"
        )
        serializer = CategoryTreeSerializer(root_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return error_response("Category not found", status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return error_response("Category not found", status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return error_response("Category not found", status.HTTP_404_NOT_FOUND)

        subcategories_count = category.subcategories.count()
        if subcategories_count > 0:
            return error_response(
                f"Can't delete the category as it contains {subcategories_count} subcategories",
                status.HTTP_409_CONFLICT,
            )

        products_count = category.products.count()
        if products_count > 0:
            return error_response(
                f"Can't delete the category as it contains {products_count} products",
                status.HTTP_409_CONFLICT,
            )

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        queryset = Product.objects.select_related("brand").all()

        # Фільтри згідно з README
        category_id = request.query_params.get("category_id")
        brand_id = request.query_params.get("brand_id")
        color = request.query_params.get("color")
        search = request.query_params.get("search")

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if color:
            queryset = queryset.filter(variations__color_name__iexact=color).distinct()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        serializer = ProductListSerializer(queryset, many=True)
        return Response(
            {"total": queryset.count(), "items": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return (
                Product.objects.select_related("brand", "category")
                .prefetch_related("variations")
                .get(pk=pk)
            )
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return error_response("Product not found", status.HTTP_404_NOT_FOUND)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return error_response("Product not found", status.HTTP_404_NOT_FOUND)
        serializer = ProductDetailSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return error_response("Product not found", status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
