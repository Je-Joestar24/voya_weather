"""
Home View Module
----------------
Handles the landing page display for unauthenticated users. Serves as the main entry point to the application.
"""

from django.shortcuts import render, redirect

def home_view(request):
    """
    Display the landing/home page for unauthenticated users.
    Redirects authenticated users to the dashboard.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Renders the home page for unauthenticated users, or redirects authenticated users to the dashboard.
    Context:
        status (str): Status type for message display.
        message (str): Page title/header message.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_view') 
    
    return render(request, 'unauthed/home/index.html', {
        'status': 'info',
        'message': 'HOME PAGE'
    })