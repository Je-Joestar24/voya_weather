
from core.views.authed.util  import settings, RecentView, fetch_weather

def get_recents(user, limit=3):
    """
    Get the most recent unique cities viewed by the user.
    Args:
        user (User): The current authenticated user.
        limit (int): Maximum number of recent cities to return.
    Returns:
        list: Recent city data for dashboard display.
    """
    # Get unique recent cities, most recent first
    recents_qs = (
        RecentView.objects.filter(user=user)
        .select_related('city')
        .order_by('-timestamp')
    )
    seen = set()
    recents = []
    api_key = settings.OPENWEATHER_API_KEY
    for recent in recents_qs:
        if recent.city_id not in seen:
            city = recent.city
            weather = fetch_weather(city.name, api_key)
            recents.append({
                'city': city.name,
                'country': city.country_code,
                'temp': weather['temp'] if weather else '--',
                'condition': weather['condition'] if weather else 'Unknown',
                'emoji': weather['emoji'] if weather else '🌍',
                'viewed_at': recent.timestamp,
                'id': city.id,
            })
            seen.add(recent.city_id)
        if len(recents) >= limit:
            break
    return recents
