from django.test import TestCase, Client
from django.urls import reverse
from core.models.city import City
from core.models.recents import RecentView
from django.contrib.auth import get_user_model

class RecentsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.get(username='test2')
        self.client.login(username='test2', password='test')
        # Create cities and recent views
        self.city1 = City.objects.create(openweather_id=21, name='Tokyo', country_code='JP', lat=35.6895, lon=139.6917)
        self.city2 = City.objects.create(openweather_id=22, name='London', country_code='GB', lat=51.5074, lon=-0.1278)
        RecentView.objects.create(user=self.user, city=self.city1)
        RecentView.objects.create(user=self.user, city=self.city2)

    def test_recents_display(self):
        response = self.client.get(reverse('recents_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'London')

    def test_recents_search(self):
        response = self.client.get(reverse('recents_view'), {'q': 'Tokyo'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tokyo')
        self.assertNotContains(response, 'London')