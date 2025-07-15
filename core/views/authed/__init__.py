"""
Unauthenticated Views Package Initialization

This module imports and exposes all views that are accessible to
unauthenticated users. These views handle the public-facing pages
of the application before user login.

Imported Views:
- about_view: Displays the about page
- home_view: Displays the landing/home page
- login_view: Displays the login form
- signup_view: Displays the registration form
"""

from .dashboard import *
from .recent import *
from .saved import *
from .search import *
from .profile import *
from .favorites import *
from .details import *