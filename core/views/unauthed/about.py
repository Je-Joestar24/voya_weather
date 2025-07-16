"""
About View Module
-----------------
Handles the about page display for unauthenticated users, providing information about the application and its features.
"""

from django.shortcuts import render, redirect

def about_view(request):
    """
    Display the about page for unauthenticated users.
    Redirects authenticated users to the dashboard.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Renders the about page for unauthenticated users, or redirects authenticated users to the dashboard.
    Context:
        status (str): Status type for message display.
        message (str): Page title/header message.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_view') 

    return render(request, 'unauthed/about/index.html', {
        'status': 'info',
        'message': 'ABOUT PAGE'
    })