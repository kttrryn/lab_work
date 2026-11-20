from django.urls import reverse
from rest_framework import status


# --- Позитивні сценарії ---

def test_get_brands_list_public(api_client, brands_data):
    url = '/api/v1/brands'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


def test_get_brand_detail_public(api_client, brands_data):
    brand = brands_data['with_products']
    url = reverse('brand-detail', kwargs={'pk': brand.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'MAC'


def test_create_brand_authenticated(auth_client, db):
    url = '/api/v1/brands'
    payload = {'name': 'Dior', 'description': 'Люксова косметика'}
    response = auth_client.post(url, payload, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'Dior'


def test_update_brand_authenticated(auth_client, brands_data):
    brand = brands_data['empty']
    url = reverse('brand-detail', kwargs={'pk': brand.id})
    payload = {'name': 'Updated Brand', 'description': 'Новий опис'}
    response = auth_client.put(url, payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Updated Brand'


def test_delete_empty_brand_authenticated(auth_client, brands_data):
    brand = brands_data['empty']
    url = reverse('brand-detail', kwargs={'pk': brand.id})
    response = auth_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


# --- Негативні сценарії ---

def test_create_brand_unauthenticated(api_client, db):
    url = '/api/v1/brands'
    payload = {'name': 'Chanel'}
    response = api_client.post(url, payload, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_brand_invalid_data(auth_client, db):
    url = '/api/v1/brands'
    response = auth_client.post(url, {'name': ''}, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_non_existent_brand(api_client, db):
    url = reverse('brand-detail', kwargs={'pk': 9999})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_brand_with_products_conflict(auth_client, brands_data):
    brand = brands_data['with_products']
    url = reverse('brand-detail', kwargs={'pk': brand.id})
    response = auth_client.delete(url)

    assert response.status_code == status.HTTP_409_CONFLICT


def test_delete_non_existent_brand(auth_client, db):
    url = reverse('brand-detail', kwargs={'pk': 9999})
    response = auth_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

