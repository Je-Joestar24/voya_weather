"""
Login View Module

This module handles user authentication through both username and email.
It provides a flexible login system that allows users to authenticate
using either their username or email address.
"""

from .utils import render, redirect, User, authenticate, login, messages

def login_process(request):
    """
    Handle user login process with support for both username and email authentication.
    
    Args:
        request (HttpRequest): The HTTP request object containing POST data
        
    Returns:
        HttpResponse: Redirects to search page if authenticated,
                     renders login page with error if authentication fails
        
    Process:
        1. Checks if user is already authenticated
        2. Attempts authentication with username
        3. If username fails, attempts authentication with email
        4. On success, redirects to next URL or search page
        5. On failure, displays error message
    """
    if request.user.is_authenticated:
        return redirect('dashboard_view') 

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to authenticate with username
        user = authenticate(request, username=username_or_email, password=password)
        
        # If authentication fails, try with email
        if user is None:
            try:
                # Get user by email
                user_obj = User.objects.get(email=username_or_email)
                # Try to authenticate with email
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/dashboard/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username/email or password')
            return render(request, 'unauthed/login/index.html', {'error': True})
    
    return render(request, 'unauthed/login/index.html')