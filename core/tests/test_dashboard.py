from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth import get_user_model

User = get_user_model()

# class DashboardViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             password='password'
#         )

#     @patch('requests.get')
#     def test_dashboard_view_weather_context(self, mock_get):
#         mock_get.side_effect = [
#             MockResponse({
#                 'main': {'temp': 30},
#                 'weather': [{'description': 'clear sky', 'icon': '01d'}]
#             }, 200),
#             MockResponse({
#                 'main': {'temp': 25},
#                 'weather': [{'description': 'few clouds', 'icon': '02d'}]
#             }, 200),
#             MockResponse({
#                 'main': {'temp': 20},
#                 'weather': [{'description': 'scattered clouds', 'icon': '03d'}]
#             }, 200),
#         ]

#         logged_in = self.client.login(username='testuser', password='password')
#         self.assertTrue(logged_in)

#         response = self.client.get(reverse('dashboard_view'))  
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('top_weather', response.context)
#         self.assertEqual(len(response.context['top_weather']), 3)

# class MockResponse:
#     def __init__(self, json_data, status_code):
#         self._json = json_data
#         self.status_code = status_code

#     def json(self):
#         return self._json
