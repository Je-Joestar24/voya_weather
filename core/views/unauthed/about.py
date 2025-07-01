"""
About View Module

This module handles the about page display for unauthenticated users.
It provides information about the application and its features.
"""

from django.shortcuts import render, redirect

def about_view(request):
    """
    Display the about page for unauthenticated users.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Renders about page or redirects to search if authenticated
        
    Context:
        status (str): Status type for message display
        message (str): Page title/header message
    """
    # if request.user.is_authenticated:
    #     return redirect('search_book_view') 

    return render(request, 'unauthed/about/index.html', {
        'status': 'info',
        'message': 'ABOUT PAGE'
        })