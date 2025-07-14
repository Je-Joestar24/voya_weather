"""
Signup View Module

This module handles the display of the registration form for new users.
It provides the initial interface for user registration.
"""

from django.shortcuts import render, redirect
    
def signup_view(request):
    """
    Display the registration form for new users.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Renders signup page or redirects to search if authenticated
        
    Context:
        status (str): Status type for message display
        message (str): Page title/header message
    """
    if request.user.is_authenticated:
        return redirect('search_book_view') 

    return render(request, 'unauthed/signup/index.html', {
        'status': 'info',
        'message': 'Welcome to Jejo Book Collector'
    })