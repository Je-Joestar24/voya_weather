"""
Favorites View Module
---------------------
Handles the display and management of user's favorite places, including search, add, and remove actions.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.views.authed.util import FavoritePlace, Q, settings, fetch_weather
import logging

logger = logging.getLogger(__name__)

class FavoritePlacesView(LoginRequiredMixin, TemplateView):
    """
    Display the user's favorite places, with optional search functionality.
    Inherits from Django's TemplateView and requires authentication.
    """
    template_name = 'authed/favorites/index.html'

    def get_context_data(self, **kwargs):
        """
        Build context for the favorites page, including search and weather data.
        Returns:
            dict: Context for template rendering.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        search_query = self.request.GET.get('q', '').strip()

        # Get all favorite places for the user
        favorites_qs = (
            FavoritePlace.objects.filter(user=user)
            .select_related('city')
            .order_by('-timestamp')
        )

        # Search
        if search_query:
            favorites_qs = favorites_qs.filter(
                Q(city__name__icontains=search_query) |
                Q(city__country_code__icontains=search_query)
            )

        # Prepare data for template
        api_key = settings.OPENWEATHER_API_KEY
        places = []
        for favorite in favorites_qs:
            city = favorite.city
            weather = fetch_weather(city.name, api_key)
            if weather:
                temp = weather['temp']
                condition = weather['condition']
                emoji = weather['emoji']
            else:
                temp = '--'
                condition = 'Unknown'
                emoji = '🌍'
            places.append({
                'id': city.id,
                'city': city.name,
                'temp': temp,
                'condition': condition,
                'emoji': emoji,
                'favorited_at': favorite.timestamp,
            })

        context.update({
            'places': places,
            'search_query': search_query,
            'status': 'info',
            'message': 'FAVORITES PAGE'
        })
        return context