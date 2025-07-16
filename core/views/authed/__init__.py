"""
Authenticated Views Package Initialization

This package imports and exposes all views that are accessible to authenticated (logged-in) users. These views handle the core, personalized, and data-driven pages of the application after user login.

Imported Views:
- dashboard_view: Displays the user dashboard
- recents_view: Shows recently viewed places
- saved_places_view: Manages saved places
- search_places_view: Search and add new places
- profile_view: User profile management
- favorite_places_view: Manages favorite places
- place_details_view: Detailed weather for a city
"""

from .dashboard import *
from .recent import *
from .saved import *
from .search import *
from .profile import *
from .favorites import *
from .details import *