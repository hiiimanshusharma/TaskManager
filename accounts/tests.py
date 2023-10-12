from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .views import LoginView, RegisterView
from .serializers import RegisterSerializer, LoginSerializer


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "password": "password123"
        }
        response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="johndoe").exists())

    def test_register_user_missing_data(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            # Missing username and password
        }
        response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(response.status_code, 400)

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

    def test_login_valid_user(self):
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(reverse("login"), data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data["data"]["token"])

    def test_login_invalid_user(self):
        data = {
            "username": "nonexistentuser",
            "password": "invalidpassword"
        }
        response = self.client.post(reverse("login"), data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "invalid credentials")
