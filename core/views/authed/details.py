"""
Details View Module
-------------------
Handles the display of detailed weather information for a specific city, including live API fetch and recent view tracking.
"""

from core.views.authed.util import render, get_object_or_404, login_required, settings, requests, City, cache_page, RecentView,  timezone

@cache_page(60 * 5)        # 5 minutes
@login_required
def place_details_view(request, city_id):
    """
    Display detailed weather information for a specific city.
    Tracks the city as recently viewed by the user.
    Args:
        request (HttpRequest): The HTTP request object.
        city_id (int): The ID of the city to display.
    Returns:
        HttpResponse: Renders the details page with weather data.
    """
    city = get_object_or_404(City, id=city_id)
    api_key = settings.OPENWEATHER_API_KEY

    # --- RECENT VIEW LOGIC ---
    # Move to top or create if not exists
    recent, created = RecentView.objects.get_or_create(user=request.user, city=city)
    if not created:
        # Already exists, update timestamp to now
        recent.timestamp = timezone.now()
        recent.save(update_fields=['timestamp'])
    # --- END RECENT VIEW LOGIC ---

    # Prefer openweather_id, fallback to name+country
    params = {
        'appid': api_key,
        'units': 'metric'
    }
    if city.openweather_id:
        params['id'] = city.openweather_id
    else:
        params['q'] = f"{city.name},{city.country_code}"

    weather_data = {}
    try:
        response = requests.get(settings.WEATHER_API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temp': round(data['main']['temp']),
            'condition': data['weather'][0]['description'].capitalize(),
            'emoji': get_emoji(data['weather'][0]['main']),
            'lat': data['coord']['lat'],
            'lon': data['coord']['lon'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main']['pressure'],
            'feels_like': round(data['main']['feels_like']),
        }
    except Exception:
        weather_data = {
            'city': city.name,
            'country': city.country_code,
            'temp': '--',
            'condition': 'Unavailable',
            'emoji': '🌍',
            'lat': city.lat,
            'lon': city.lon,
            'humidity': '--',
            'wind_speed': '--',
            'pressure': '--',
            'feels_like': '--',
        }

    return render(request, 'authed/details/index.html', {
        'status': 'info',
        'message': 'VIEW DETAILS',
        'place': weather_data,
    })

def get_emoji(condition):
    """
    Map weather condition strings to emoji for display.
    Args:
        condition (str): Weather condition (e.g., 'Rain', 'Clear').
    Returns:
        str: Corresponding emoji character.
    """
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
    return EMOJI_MAP.get(condition, '🌍')