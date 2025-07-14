# tests/test_signup.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpProcessTests(TestCase):
    signup_url = reverse("signup")               
    dashboard_url = reverse("dashboard_view")    

    def setUp(self):
        self.payload = {
            "fullname": "Jane Doe",
            "email": "jane@example.com",
            "username": "janedoe",
            "password": "Secret123!",
            "confirm_password": "Secret123!",
        }

    def test_get_signup_returns_200(self):
        resp = self.client.get(self.signup_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "unauthed/signup/index.html")

    def test_authenticated_user_redirects(self):
        user = User.objects.create_user(
            username="loggedin",
            email="loggedin@example.com",
            password="pass1234"
        )
        self.client.login(username="loggedin", password="pass1234")
        resp = self.client.get(self.signup_url)
        self.assertRedirects(resp, self.dashboard_url)

    def test_password_mismatch_shows_error(self):
        bad_payload = self.payload | {"confirm_password": "notmatching"}
        resp = self.client.post(self.signup_url, bad_payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Passwords do not match")
        self.assertFalse(User.objects.filter(username="janedoe").exists())

    def test_duplicate_email_shows_error(self):
        User.objects.create_user(
            username="someone",
            email="jane@example.com",
            password="pass1234"
        )
        resp = self.client.post(self.signup_url, self.payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Email already exists")

    def test_duplicate_username_shows_error(self):
        User.objects.create_user(
            username="janedoe",
            email="unique@example.com",
            password="pass1234"
        )
        resp = self.client.post(self.signup_url, self.payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Username already exists")

    def test_signup_success_creates_user_and_redirects(self):
        resp = self.client.post(self.signup_url, self.payload)
        self.assertTrue(User.objects.filter(username="janedoe").exists())
        self.assertRedirects(resp, self.dashboard_url)
