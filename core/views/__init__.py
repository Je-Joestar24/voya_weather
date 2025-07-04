"""
Main Views Package Initialization

This module serves as the central import point for all view modules in the application.
It organizes views into three main categories:

1. Unauthenticated Views: Public-facing pages (home, about, login, signup)
2. Book Views: Core functionality for book management (search, view, collection, recent)
3. Authentication Views: User management (login, logout, profile, signup)

This structure ensures proper separation of concerns and maintains
a clear organization of the application's view logic.
"""

from .unauthed import *
from .authed import *