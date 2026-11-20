import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from catalog.models import Brand, Category, Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_superuser(
        username='testuser',
        email='test@example.com',
        password='StrongPassword123!'
    )


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def brands_data(db):
    brand_with_products = Brand.objects.create(
        name='MAC',
        description='Професійна косметика'
    )
    empty_brand = Brand.objects.create(
        name='Empty Brand',
        description='Бренд без товарів'
    )
    category = Category.objects.create(name='Губи')
    Product.objects.create(
        sku='MAC-001',
        name='Matte Lipstick',
        description='Червона помада',
        price=450.00,
        brand=brand_with_products,
        category=category
    )
    return {
        'with_products': brand_with_products,
        'empty': empty_brand,
    }
