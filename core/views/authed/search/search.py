"""
Search Places View Module
-------------------------
Handles searching for cities, displaying weather data, and saving/unsaving places for authenticated users.
"""
from core.views.authed.util  import get_object_or_404, City, SavedPlace, redirect, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.views.authed.util  import settings
from .search_helper import CITIES, get_or_create_city_with_weather

class SearchPlacesView(LoginRequiredMixin, TemplateView):
    """
    Display the search places page, showing weather for default or searched cities.
    Inherits from Django's TemplateView and requires authentication.
    """
    template_name = 'authed/searchplaces/index.html'

    def get_context_data(self, **kwargs):
        """
        Build context for the search places page, including weather data for default or searched cities.
        Returns:
            dict: Context for template rendering.
        """
        context = super().get_context_data(**kwargs)
        api_key = settings.OPENWEATHER_API_KEY
        city_query = self.request.GET.get('city', '').strip()

        if not city_query:
            # Show default static cities
            weather_data = []
            for city in CITIES:
                weather = get_or_create_city_with_weather(city, api_key, self.request.user)
                if weather:
                    weather_data.append(weather)
            context.update({
                'status': 'info',
                'message': 'SEARCH PLACES',
                'places': weather_data[:9]
            })
            return context

        # User searched for a city
        weather = get_or_create_city_with_weather(city_query, api_key, self.request.user)
        if weather:
            places = [weather]
            status = 'success'
            message = f"Results for '{city_query}'"
        else:
            places = []
            status = 'error'
            message = f"No weather data found for '{city_query}'."

        context.update({
            'status': status,
            'message': message,
            'places': places,
        })
        return context