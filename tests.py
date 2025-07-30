from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

from ads.models import Ad, Comment


User = get_user_model()


class UserFlowTestCase(TestCase):
    def setUp(self):
        self.email = 'testuser@mail.com'
        self.password = 'testpass123'
        self.client = APIClient()

        # Register user
        register_response = self.client.post('/users/register/', {
            'email': self.email,
            'password': self.password,
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '+48123456789',
            'role': 'user'
        })
        self.assertEqual(register_response.status_code, 201)

        # Login user
        token_response = self.client.post('/users/login/', {
            'email': self.email,
            'password': self.password
        })
        self.assertEqual(token_response.status_code, 200)

        # Set Authorization header
        self.token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_password_reset_flow(self):
        # Register another user for reset test
        other_email = "reset@mail.com"
        response = self.client.post('/users/register/', {
            'email': other_email,
            'password': 'resetpass123',
            'first_name': 'Reset',
            'last_name': 'User',
            'phone': '+48111222333',
            'role': 'user'
        })
        self.assertEqual(response.status_code, 201)

        reset_client = APIClient()
        response = reset_client.post(reverse('reset-password'), {"email": other_email})
        self.assertEqual(response.status_code, 200)

    def test_create_ad(self):
        response = self.client.post('/ads/', {
            "title": "Test Item",
            "price": 100,
            "description": "Test desc"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ad.objects.count(), 1)

    def test_list_ads_with_pagination(self):
        for i in range(10):
            self.client.post('/ads/', {
                "title": f"Item {i}",
                "price": i * 10,
                "description": "desc"
            })
        response = self.client.get('/ads/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 4)

    def test_create_comment(self):
        user = User.objects.get(email=self.email)
        ad = Ad.objects.create(
            title="Ad1",
            price=100,
            description="test",
            author=user
        )
        response = self.client.post(f'/ads/{ad.id}/comments/', {"text": "Nice ad!"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
