from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models.recents import RecentView
from core.models.city import City
from django.db.models import Q
from django.conf import settings
from core.views.authed.search import fetch_weather

@login_required
def recents_view(request):
    user = request.user
    search_query = request.GET.get('q', '').strip()

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

    return render(request, 'authed/recentplaces/index.html', {
        'status': 'info',
        'message': 'RECENT VIEWED PLACES',
        'places': places,
        'search_query': search_query,
    })