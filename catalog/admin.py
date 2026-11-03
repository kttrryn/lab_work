from django.contrib import admin

from .models import Brand, Category, Product, ProductVariation


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'price', 'brand', 'category')
    list_filter = ('brand', 'category')
    search_fields = ('name', 'sku')
    inlines = [ProductVariationInline]
