"""
Profile View Module

This module handles user profile management, including displaying
and updating user information. It provides both GET and POST
functionality for viewing and modifying profile data.
"""


from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    """
    Handle user profile display and updates.
    
    Args:
        request (HttpRequest): The HTTP request object containing POST data for updates
        
    Returns:
        HttpResponse: Renders profile page with user data
        
    Process:
        GET:
            - Displays current user profile information
        POST:
            - Updates user profile with new information
            - Handles validation and error cases
            - Provides feedback through messages framework
    
    Context Data:
        - fullname: User's full name
        - username: User's username
        - email: User's email address
        - id: User's ID
        - status: Current operation status
        - message: Status message for the user
    """
    user = request.user  # Get the logged-in user
    
    if request.method == 'POST':
        # Handle profile update
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        
        try:
            user.fullname = fullname
            user.email = email
            user.username = username
            user.save()
            
            messages.success(request, 'Profile updated successfully')
        except Exception as e:
            messages.error(request, str(e))
            
        return render(request, 'authed/profile/index.html', {
            'fullname': user.fullname,
            'username': user.username,
            'email': user.email,
            'id': user.id,
            'status': 'success',
            'message': 'PROFILE UPDATED'
        })

    # GET request - show profile
    context = {
        'fullname': user.fullname,
        'username': user.username,
        'email': user.email,
        'id': user.id,
        'status': 'info',
        'message': 'PROFILE PAGE'
    }

    return render(request, 'authed/profile/index.html', context)