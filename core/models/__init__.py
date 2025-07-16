"""
VoyaWeather Models Package

This package defines all database models for the VoyaWeather application, including user accounts, city data, and user-place relationships (saved, favorites, recents).
"""

from .user import User      # Custom user model for authentication and profile data
from .city import City      # City/location data, mapped to OpenWeather IDs
from .saved import SavedPlace      # User-saved cities
from .favorites import FavoritePlace   # User-favorited cities
from .recents import RecentView        # User's recently viewed cities

__all__ = [
    "User",
    "City",
    "SavedPlace",
    "FavoritePlace",
    "RecentView",
]