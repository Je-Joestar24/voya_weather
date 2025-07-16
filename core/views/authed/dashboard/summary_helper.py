
from core.views.authed.util  import settings, SavedPlace, RecentView, fetch_weather

def get_summary(user):
    """
    Gather summary statistics for the dashboard, including total saved places, hottest/coldest saved city, and last viewed city.
    Args:
        user (User): The current authenticated user.
    Returns:
        dict: Summary data for dashboard display.
    """
    # Total saved places
    saved_qs = SavedPlace.objects.filter(user=user).select_related('city')
    total_saved = saved_qs.count()

    # Fetch weather for all saved cities
    api_key = settings.OPENWEATHER_API_KEY
    city_weather = []
    for saved in saved_qs:
        city = saved.city
        weather = fetch_weather(city.name, api_key)
        if weather:
            city_weather.append({
                'city': city,
                'temp': weather['temp'],
                'condition': weather['condition'],
                'emoji': weather['emoji'],
            })

    # Hottest and coldest saved city
    hottest = max(city_weather, key=lambda x: x['temp'], default=None)
    coldest = min(city_weather, key=lambda x: x['temp'], default=None)

    # Last viewed city
    last_view = (
        RecentView.objects.filter(user=user)
        .select_related('city')
        .order_by('-timestamp')
        .first()
    )
    last_viewed = None
    if last_view:
        city = last_view.city
        weather = fetch_weather(city.name, api_key)
        last_viewed = {
            'city': city,
            'temp': weather['temp'] if weather else '--',
            'condition': weather['condition'] if weather else 'Unknown',
            'emoji': weather['emoji'] if weather else '🌍',
            'ago': last_view.timestamp,
        }

    return {
        'total_saved': total_saved,
        'hottest': hottest,
        'coldest': coldest,
        'last_viewed': last_viewed,
    }
