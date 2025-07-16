"""
Main Views Package Initialization
--------------------------------
Central import point for all view modules in the VoyaWeather application.

Organizes views into three main categories:

1. Unauthenticated Views: Public-facing pages (home, about, login, signup)
2. Authenticated Views: User dashboard and features (dashboard, saved, favorites, recent, profile, etc.)
3. Authentication/User Views: User management (login, logout, profile, signup, password, etc.)

This structure ensures clear separation of concerns and maintainable organization of the application's view logic.
"""

from .unauthed import *
from .authed import *
from .auths import *