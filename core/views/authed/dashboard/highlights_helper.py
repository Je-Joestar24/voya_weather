
from core.views.authed.util  import settings, SavedPlace, FavoritePlace, RecentView, fetch_weather

def get_highlights(user, limit=4):
    """
    Get highlights of the user's favorite places for dashboard display.
    Args:
        user (User): The current authenticated user.
        limit (int): Maximum number of highlights to return.
    Returns:
        list: Highlighted favorite city data.
    """
    # Top N favorite places, most recently favorited
    favorites_qs = (
        FavoritePlace.objects.filter(user=user)
        .select_related('city')
        .order_by('-timestamp')[:limit]
    )
    api_key = settings.OPENWEATHER_API_KEY
    highlights = []
    for fav in favorites_qs:
        city = fav.city
        weather = fetch_weather(city.name, api_key)
        highlights.append({
            'city': city.name,
            'temp': weather['temp'] if weather else '--',
            'condition': weather['condition'] if weather else 'Unknown',
            'emoji': weather['emoji'] if weather else '🌍',
            'id': city.id,
        })
    return highlights
