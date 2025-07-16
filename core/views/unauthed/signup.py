"""
Signup View Module
------------------
Handles the display of the registration form for new users, providing the initial interface for user registration.
"""

from django.shortcuts import render, redirect
    
def signup_view(request):
    """
    Display the registration form for new users.
    Redirects authenticated users to the dashboard.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Renders the signup page for unauthenticated users, or redirects authenticated users to the dashboard.
    Context:
        status (str): Status type for message display.
        message (str): Page title/header message.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_view') 

    return render(request, 'unauthed/signup/index.html', {
        'status': 'info',
        'message': 'Welcome to Jejo Book Collector'
    })