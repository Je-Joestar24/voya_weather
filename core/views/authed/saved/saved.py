"""
Saved Places View Module
------------------------
Handles the display and management of user's saved places, including search, add/remove, and favorite toggling.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.views.authed.util import SavedPlace, FavoritePlace, Q, fetch_weather, settings
import logging

logger = logging.getLogger(__name__)

class SavedPlacesView(LoginRequiredMixin, TemplateView):
    """
    Display the user's saved places, with optional search functionality.
    Inherits from Django's TemplateView and requires authentication.
    """
    template_name = 'authed/savedplaces/index.html'

    def get_context_data(self, **kwargs):
        """
        Build context for the saved places page, including search and weather data.
        Returns:
            dict: Context for template rendering.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        search_query = self.request.GET.get('q', '').strip()

        # Get all saved places for the user
        saved_qs = SavedPlace.objects.filter(user=user).select_related('city').order_by('-timestamp')

        # Search
        if search_query:
            saved_qs = saved_qs.filter(
                Q(city__name__icontains=search_query) |
                Q(city__country_code__icontains=search_query)
            )

        # Prepare data for template
        places = []
        api_key = settings.OPENWEATHER_API_KEY
        for saved in saved_qs:
            city = saved.city
            weather = fetch_weather(city.name, api_key)
            if weather:
                temp = weather['temp']
                condition = weather['condition']
                emoji = weather['emoji']
            else:
                temp = '--'
                condition = 'Unknown'
                emoji = '🌍'
            is_favorite = FavoritePlace.objects.filter(user=user, city=city).exists()
            places.append({
                'id': city.id,
                'city': city.name,
                'temp': temp,
                'condition': condition,
                'emoji': emoji,
                'is_saved': True,
                'is_favorite': is_favorite,
                'saved_at': saved.timestamp,
            })

        context.update({
            'places': places,
            'search_query': search_query,
            'has_places': bool(places),
            'status': 'info',
            'message': 'PROFILE PAGE'
        })
        return context