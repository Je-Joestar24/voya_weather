"""
Authenticated Views Utility Module
----------------------------------
Provides shared utilities, imports, and helpers for authenticated views, including decorators, database access, and weather fetching.
"""

import logging
import requests
from typing import Optional

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError, IntegrityError
from django.db.models import Q, Max, Min
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.cache import cache_page

from requests.exceptions import RequestException

from core.models.city import City
from core.models.favorites import FavoritePlace
from core.models.recents import RecentView
from core.models.saved import SavedPlace
from core.views.authed.search import fetch_weather
