from django.urls import path

from .views import (
    BrandDetailView,
    BrandListCreateView,
    CategoryDetailView,
    CategoryListCreateView,
    ProductDetailView,
    ProductListCreateView,
)

urlpatterns = [
    path("brands", BrandListCreateView.as_view(), name="brand-list-create"),
    path("brands/<int:pk>", BrandDetailView.as_view(), name="brand-detail"),
    path("categories", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<int:pk>", CategoryDetailView.as_view(), name="category-detail"),
    path("products", ProductListCreateView.as_view(), name="product-list-create"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product-detail"),
]
