"""
Favorites View Module
---------------------
Handles the display and management of user's favorite places, including search, add, and remove actions.
"""

from core.views.authed.util import render, login_required, FavoritePlace, Q, settings, logging, login_required, fetch_weather

logger = logging.getLogger(__name__)

@login_required
def favorite_places_view(request):
    """
    Display the user's favorite places, with optional search functionality.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Renders the favorites page with context data.
    """
    user = request.user
    search_query = request.GET.get('q', '').strip()

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

    context = {
        'places': places,
        'search_query': search_query,
        'status': 'info',
        'message': 'FAVORITES PAGE'
    }
    return render(request, 'authed/favorites/index.html', context)