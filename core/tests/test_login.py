# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class LoginProcessTests(TestCase):
#     login_url = reverse("login")              
#     dashboard_url = reverse("dashboard_view")

#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="test2",
#             email="test@gmail.com",
#             password="test"
#         )

#     def test_get_login_returns_200(self):
#         resp = self.client.get(self.login_url)
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, "unauthed/login/index.html")

#     def test_authenticated_user_redirects(self):
#         self.client.login(username="test2", password="test")
#         resp = self.client.get(self.login_url)
#         self.assertRedirects(resp, self.dashboard_url)

#     def test_invalid_login_shows_error(self):
#         resp = self.client.post(self.login_url, {
#             "username": "wronguser",
#             "password": "wrongpass"
#         })
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, "unauthed/login/index.html")
#         self.assertContains(resp, "Invalid username/email or password")

#     def test_valid_login_with_username_redirects(self):
#         resp = self.client.post(self.login_url, {
#             "username": "test2",
#             "password": "test"
#         })
#         self.assertRedirects(resp, self.dashboard_url)

#     def test_valid_login_with_email_redirects(self):
#         resp = self.client.post(self.login_url, {
#             "username": "test@gmail.com",  
#             "password": "test"
#         })
#         self.assertRedirects(resp, self.dashboard_url)

#     def test_login_redirects_to_next_url(self):
#         next_url = reverse("profile_view")  
#         resp = self.client.post(f"{self.login_url}?next={next_url}", {
#             "username": "test2",
#             "password": "test"
#         })
#         self.assertRedirects(resp, next_url)