"""
Search Places View Module
-------------------------
Handles searching for cities, displaying weather data, and saving/unsaving places for authenticated users.
"""

from core.views.authed.util  import settings, requests, login_required, render, redirect, get_object_or_404, RequestException, City, SavedPlace, Optional

CITIES = [
    'Nuuk', 'Ormoc City', 'Cebu City', 'Mandaue City',
    'Sorsogon City', 'Chicago', 'Moscow', 'Copenhagen', 'Warsaw'
]

EMOJI_MAP = {
    'Snow': '❄️',
    'Rain': '🌧️',
    'Clouds': '☁️',
    'Clear': '☀️',
    'Thunderstorm': '🌩️',
    'Drizzle': '🌦️',
    'Mist': '🌫️',
    'Fog': '🌁',
}

def fetch_weather(city, api_key):
    """
    Fetch live weather data for a city using the OpenWeather API.
    Args:
        city (str): City name.
        api_key (str): OpenWeather API key.
    Returns:
        dict or None: Weather data dictionary or None if not found.
    """
    try:
        response = requests.get(
            settings.WEATHER_API_URL,
            params={
                'q': city,
                'appid': api_key,
                'units': 'metric'
            },
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        condition = data['weather'][0]['main']
        emoji = EMOJI_MAP.get(condition, '🌍')  # default if not matched

        return {
            'city': city,
            'temp': round(data['main']['temp']),
            'condition': data['weather'][0]['description'].capitalize(),
            'emoji': emoji
        }
    except (RequestException, KeyError, IndexError):
        return None
    
def get_or_create_city_with_weather(city_name: str, api_key: str, user) -> Optional[dict]:
    """
    Fetch weather and persist city if needed. Return weather + city_id, or None.
    Args:
        city_name (str): City name.
        api_key (str): OpenWeather API key.
        user (User): The current authenticated user.
    Returns:
        dict or None: Weather data with city_id, or None if not found.
    """
    weather = fetch_weather(city_name, api_key)
    if not weather:
        return None

    try:
        response = requests.get(
            settings.WEATHER_API_URL,
            params={
                'q': city_name,
                'appid': api_key,
                'units': 'metric',
            },
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

        city_obj, _ = City.objects.get_or_create(
            openweather_id=data['id'],
            defaults={
                'name': data['name'],
                'country_code': data['sys']['country'],
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon'],
            }
        )
        city_id = city_obj.id
        is_saved = SavedPlace.objects.filter(city_id=city_id, user=user).exists()
        weather["is_saved"] = is_saved
    except Exception:
        city_id = None

    weather["id"] = city_id
    return weather

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