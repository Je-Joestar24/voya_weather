"""
Search Places View Module
-------------------------
Handles searching for cities, displaying weather data, and saving/unsaving places for authenticated users.
"""

from core.views.authed.util  import settings, requests, login_required, render, redirect, get_object_or_404, RequestException, City, SavedPlace, Optional
from .search_helper import CITIES, get_or_create_city_with_weather

@login_required
def search_places_view(request):
    """
    Display the search places page, showing weather for default or searched cities.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Renders the search places page with context data.
    """
    api_key = settings.OPENWEATHER_API_KEY
    city_query = request.GET.get('city', '').strip()

    if not city_query:
        # Show default static cities
        weather_data = []
        for city in CITIES:
            weather = get_or_create_city_with_weather(city, api_key, request.user)
            if weather:
                weather_data.append(weather)
        return render(request, 'authed/searchplaces/index.html', {
            'status': 'info',
            'message': 'SEARCH PLACES',
            'places': weather_data[:9]
        })

    # User searched for a city
    weather = get_or_create_city_with_weather(city_query, api_key, request.user)
    if weather:
        places = [weather]
        status = 'success'
        message = f"Results for '{city_query}'"
    else:
        places = []
        status = 'error'
        message = f"No weather data found for '{city_query}'."

    return render(request, 'authed/searchplaces/index.html', {
        'status': status,
        'message': message,
        'places': places,
    })

@login_required
def toggle_save_place(request, city_id):
    """
    Add or remove a city from the user's saved places. Redirects to search places view.
    Args:
        request (HttpRequest): The HTTP request object.
        city_id (int): The ID of the city to toggle as saved.
    Returns:
        HttpResponse: Redirects to the search places page.
    """
    city = get_object_or_404(City, id=city_id)
    user = request.user
    saved, created = SavedPlace.objects.get_or_create(user=user, city=city)
    if not created:
        # Already saved, so unsave (delete)
        saved.delete()
    return redirect('search_places_view')