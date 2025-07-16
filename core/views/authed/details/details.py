"""
Details View Module
-------------------
Handles the display of detailed weather information for a specific city, including live API fetch and recent view tracking.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from core.views.authed.util import get_object_or_404, settings, requests, City, RecentView, timezone
from .emoji_helper import get_emoji

@method_decorator(cache_page(60 * 5), name='dispatch')
class PlaceDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'authed/details/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_id = self.kwargs['city_id']
        request = self.request
        city = get_object_or_404(City, id=city_id)
        api_key = settings.OPENWEATHER_API_KEY

        # --- RECENT VIEW LOGIC ---
        recent, created = RecentView.objects.get_or_create(user=request.user, city=city)
        if not created:
            recent.timestamp = timezone.now()
            recent.save(update_fields=['timestamp'])
        # --- END RECENT VIEW LOGIC ---

        params = {
            'appid': api_key,
            'units': 'metric'
        }
        if city.openweather_id:
            params['id'] = city.openweather_id
        else:
            params['q'] = f"{city.name},{city.country_code}"

        weather_data = {}
        try:
            response = requests.get(settings.WEATHER_API_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temp': round(data['main']['temp']),
                'condition': data['weather'][0]['description'].capitalize(),
                'emoji': get_emoji(data['weather'][0]['main']),
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'pressure': data['main']['pressure'],
                'feels_like': round(data['main']['feels_like']),
            }
        except Exception:
            weather_data = {
                'city': city.name,
                'country': city.country_code,
                'temp': '--',
                'condition': 'Unavailable',
                'emoji': '🌍',
                'lat': city.lat,
                'lon': city.lon,
                'humidity': '--',
                'wind_speed': '--',
                'pressure': '--',
                'feels_like': '--',
            }

        context.update({
            'status': 'info',
            'message': 'VIEW DETAILS',
            'place': weather_data,
        })
        return context