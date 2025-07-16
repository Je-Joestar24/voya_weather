"""
Login View Module
-----------------
Handles the display of the login form for unauthenticated users, providing the initial interface for user authentication.
"""

from django.shortcuts import render, redirect
    
def login_view(request):
    """
    Display the login form for unauthenticated users.
    Redirects authenticated users to the dashboard.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Renders the login page for unauthenticated users, or redirects authenticated users to the dashboard.
    Context:
        status (str): Status type for message display.
        message (str): Page title/header message.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_view') 

    return render(request, 'unauthed/login/index.html', {
        'status': 'info',
        'message': 'LOGIN NOW!'
    })