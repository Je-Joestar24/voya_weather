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