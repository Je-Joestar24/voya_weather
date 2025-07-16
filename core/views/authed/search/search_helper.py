"""
Search Places View Module
-------------------------
Handles searching for cities, displaying weather data, and saving/unsaving places for authenticated users.
"""

from core.views.authed.util  import settings, requests, RequestException, City, SavedPlace, Optional

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