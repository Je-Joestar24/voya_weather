"""
Recent Views Module
-------------------
Handles the display of recently viewed places for authenticated users, including search and deduplication logic.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.views.authed.util import RecentView, settings, fetch_weather

class RecentsView(LoginRequiredMixin, TemplateView):
    """
    Display the user's recently viewed places, with optional search functionality.
    Inherits from Django's TemplateView and requires authentication.
    """
    template_name = 'authed/recentplaces/index.html'

    def get_context_data(self, **kwargs):
        """
        Build context for the recent places page, including search and deduplication.
        Returns:
            dict: Context for template rendering.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        search_query = self.request.GET.get('q', '').strip()

        # Get all recent views for the user, newest first, no duplicates (latest only)
        recents_qs = (
            RecentView.objects.filter(user=user)
            .select_related('city')
            .order_by('-timestamp')
        )

        # Remove duplicates: keep only the latest for each city
        seen = set()
        unique_recents = []
        for recent in recents_qs:
            if recent.city_id not in seen:
                unique_recents.append(recent)
                seen.add(recent.city_id)

        # Search
        if search_query:
            unique_recents = [
                r for r in unique_recents
                if search_query.lower() in r.city.name.lower() or search_query.lower() in r.city.country_code.lower()
            ]

        # Prepare data for template
        api_key = settings.OPENWEATHER_API_KEY
        places = []
        for recent in unique_recents:
            city = recent.city
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
                'city': f"{city.name}, {city.country_code}",
                'temp': temp,
                'condition': condition,
                'emoji': emoji,
                'viewed_at': recent.timestamp,
            })

        context.update({
            'status': 'info',
            'message': 'RECENT VIEWED PLACES',
            'places': places,
            'search_query': search_query,
        })
        return context