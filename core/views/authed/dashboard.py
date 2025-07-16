"""
Dashboard View Module
---------------------
Handles the user dashboard, including summary statistics, recent activity, and highlights of favorite/saved places.
"""

from core.views.authed.util  import render, login_required, settings, SavedPlace, FavoritePlace, RecentView, fetch_weather

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

@login_required
def dashboard_view(request):
    """
    Render the dashboard page for authenticated users, including summary, recents, and highlights.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Renders the dashboard template with context data.
    """
    user = request.user
    summary = get_summary(user)
    recents = get_recents(user)
    highlights = get_highlights(user)

    return render(request, 'authed/dashboard/index.html', {
        'status': 'info',
        'message': 'DASHBOARD',
        'summary': summary,
        'recents': recents,
        'highlights': highlights,
    })