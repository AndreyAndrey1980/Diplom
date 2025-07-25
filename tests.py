import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

from ads.models import Ad, Comment


User = get_user_model()


@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        return User.objects.create_user(password='testpass123', **kwargs)
    return create_user


@pytest.fixture
def authenticated_client(user_factory):
    user = user_factory(email='testuser@mail.com')
    client = APIClient()
    response = client.post('/token/', {'email': user.email, 'password': 'testpass123'})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    return client

@pytest.mark.django_db
def test_password_reset_flow(user_factory):
    user = user_factory(email="test@mail.com")
    client = APIClient()
    response = client.post(reverse('reset-password'), {"email": user.email})
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_ad(authenticated_client):
    response = authenticated_client.post('/ads/', {
        "title": "Test Item",
        "price": 100,
        "description": "Test desc"
    })
    assert response.status_code == 201
    assert Ad.objects.count() == 1


@pytest.mark.django_db
def test_password_reset_flow(user_factory):
    user = user_factory(email="test@mail.com")
    client = APIClient()
    response = client.post(reverse('reset-password'), {"email": user.email})
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_ad(authenticated_client):
    response = authenticated_client.post('/ads/', {
        "title": "Test Item",
        "price": 100,
        "description": "Test desc"
    })
    assert response.status_code == 201
    assert Ad.objects.count() == 1


@pytest.mark.django_db
def test_list_ads_with_pagination(authenticated_client):
    for i in range(10):
        authenticated_client.post('/ads/', {
            "title": f"Item {i}",
            "price": i * 10,
            "description": "desc"
        })
    response = authenticated_client.get('/ads/')
    assert response.status_code == 200
    assert 'results' in response.data
    assert len(response.data['results']) <= 4


@pytest.mark.django_db
def test_create_comment(authenticated_client):
    ad = Ad.objects.create(title="Ad1", price=100, description="test", author=User.objects.first())
    response = authenticated_client.post(f'/ads/{ad.id}/comments/', {"text": "Nice ad!"})
    assert response.status_code == 201
    assert Comment.objects.count() == 1
