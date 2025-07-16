from core.views.authed.util import login_required, render, SavedPlace, FavoritePlace, Q, fetch_weather, settings, logging, login_required

logger = logging.getLogger(__name__)

@login_required
def saved_places_view(request):
    """
    Display the user's saved places, with optional search functionality.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Renders the saved places page with context data.
    """
    user = request.user
    search_query = request.GET.get('q', '').strip()

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
        # Fetch live weather for this city
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

    # If sorted by hottest/coldest, places is already a list, else it's a queryset
    if isinstance(places, list):
        pass
    else:
        places = list(places)

    context = {
        'places': places,
        'search_query': search_query,
        'has_places': bool(places),
        'status': 'info',
        'message': 'PROFILE PAGE'
    }
    return render(request, 'authed/savedplaces/index.html', context)