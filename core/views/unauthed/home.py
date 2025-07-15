"""
Home View Module

This module handles the landing page display for unauthenticated users.
It serves as the main entry point to the application.
"""

from django.shortcuts import render, redirect

def home_view(request):
    """
    Display the landing/home page for unauthenticated users.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Renders home page or redirects to search if authenticated
        
    Context:
        status (str): Status type for message display
        message (str): Page title/header message
    """
    if request.user.is_authenticated:
        return redirect('dashboard_view') 
        
    return render(request, 'unauthed/home/index.html', {
        'status': 'info',
        'message': 'HOME PAGE'
        })