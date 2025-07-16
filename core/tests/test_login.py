"""
Login Process Tests
-------------------
Tests for the login view, including authentication, error handling, and redirection logic.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginProcessTests(TestCase):
    """
    Test suite for login functionality:
    - GET login page
    - Login with username or email
    - Error handling for invalid credentials
    - Redirection for authenticated users and next URL
    """
    login_url = reverse("login")              
    dashboard_url = reverse("dashboard_view")

    def setUp(self):
        """Create a test user for login tests."""
        self.user = User.objects.create_user(
            username="test2",
            email="test@gmail.com",
            password="test"
        )

    def test_get_login_returns_200(self):
        """GET /login returns 200 and uses the correct template."""
        resp = self.client.get(self.login_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "unauthed/login/index.html")

    def test_authenticated_user_redirects(self):
        """Authenticated user is redirected from login to dashboard."""
        self.client.login(username="test2", password="test")
        resp = self.client.get(self.login_url)
        self.assertRedirects(resp, self.dashboard_url)

    def test_invalid_login_shows_error(self):
        """Invalid credentials show error message and do not log in."""
        resp = self.client.post(self.login_url, {
            "username": "wronguser",
            "password": "wrongpass"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "unauthed/login/index.html")
        self.assertContains(resp, "Invalid username/email or password")

    def test_valid_login_with_username_redirects(self):
        """Valid login with username redirects to dashboard."""
        resp = self.client.post(self.login_url, {
            "username": "test2",
            "password": "test"
        })
        self.assertRedirects(resp, self.dashboard_url)

    def test_valid_login_with_email_redirects(self):
        """Valid login with email redirects to dashboard."""
        resp = self.client.post(self.login_url, {
            "username": "test@gmail.com",  
            "password": "test"
        })
        self.assertRedirects(resp, self.dashboard_url)

    def test_login_redirects_to_next_url(self):
        """Login with ?next param redirects to the specified next URL."""
        next_url = reverse("profile_view")  
        resp = self.client.post(f"{self.login_url}?next={next_url}", {
            "username": "test2",
            "password": "test"
        })
        self.assertRedirects(resp, next_url)