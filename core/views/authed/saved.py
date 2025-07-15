from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models.saved import SavedPlace
from core.models.favorites import FavoritePlace
from core.models.city import City
from django.db.models import Q
from core.views.authed.search import fetch_weather  # Import your fetch_weather function
from django.conf import settings

@login_required
def saved_places_view(request):
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
    }
    return render(request, 'authed/savedplaces/index.html', context)

@login_required
def toggle_favorite_place(request, city_id):
    user = request.user
    city = get_object_or_404(City, id=city_id)
    favorite, created = FavoritePlace.objects.get_or_create(user=user, city=city)
    if not created:
        # Already a favorite, so remove
        favorite.delete()
    # Redirect back to saved places
    return redirect('saved_places_view')