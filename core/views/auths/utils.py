"""
Authentication Utilities Module

This module provides common utilities and imports used across authentication views.
It centralizes imports and provides access to Django's authentication components.

Imports:
- Django shortcuts: render, redirect
- Authentication: get_user_model, login, authenticate, logout
- Messages framework: messages
- Decorators: login_required
"""

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()