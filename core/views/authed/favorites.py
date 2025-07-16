from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models.favorites import FavoritePlace
from core.models.city import City
from django.db.models import Q
from django.conf import settings
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError, IntegrityError
from django.shortcuts import get_object_or_404, redirect
from core.views.authed.search import fetch_weather

logger = logging.getLogger(__name__)

@login_required
def favorite_places_view(request):
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


@login_required
def remove_favorite(request, city_id):
    """
    Remove a favorite place.  
    If the record is missing we log it but still redirect cleanly.
    """
    user = request.user
    city = get_object_or_404(City, id=city_id)

    try:
        # .filter().delete() avoids the extra get_or_create() round-trip
        deleted, _ = FavoritePlace.objects.filter(user=user, city=city).delete()
        if deleted:
            messages.info(request, f"✖ {city.name} removed from favorite places.")
        else:
            # No row found; not an error, but useful to know.
            logger.warning("Unsave called but no record for user %s / city %s", user.id, city.id)
            messages.warning(request, f"{city.name} wasn’t in your favorite places.")
    except DatabaseError as e:
        logger.error("Unsave failed for user %s / city %s: %s", user.id, city.id, e)
        messages.error(request, "Couldn’t remove the place—please try again.")

    return redirect("favorite_places_view")