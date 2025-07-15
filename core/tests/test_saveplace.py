from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import City, SavedPlace

class ToggleSavePlaceViewTest(TestCase):
    def setUp(self):
        # Create test user and city
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.city = City.objects.create(
            id=11,
            openweather_id=16970181,
            name='Ormoc City',
            country_code='PH',
            lat=11.00640,
            lon=124.60750
        )
        self.client = Client()

    def test_toggle_save_place_creates_and_deletes(self):
        # Login the user
        self.client.login(username='test2', password='test')

        # First toggle: should create a SavedPlace
        response = self.client.get(
            reverse('toggle_save_place', args=[self.city.id]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SavedPlace.objects.filter(user=self.user, city=self.city).exists())

        # Second toggle: should delete the SavedPlace
        response = self.client.get(
            reverse('toggle_save_place', args=[self.city.id]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(SavedPlace.objects.filter(user=self.user, city=self.city).exists())
