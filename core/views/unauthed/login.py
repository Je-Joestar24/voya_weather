"""
Login View Module

This module handles the display of the login form for unauthenticated users.
It provides the initial interface for user authentication.
"""

from django.shortcuts import render, redirect
    
def login_view(request):
    """
    Display the login form for unauthenticated users.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Renders login page or redirects to search if authenticated
        
    Context:
        status (str): Status type for message display
        message (str): Page title/header message
    """
    if request.user.is_authenticated:
        return redirect('search_book_view') 

    return render(request, 'unauthed/login/index.html', {
        'status': 'info',
        'message': 'LOGIN NOW!'
    })