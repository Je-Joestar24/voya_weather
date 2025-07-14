"""
Signup View Module

This module handles new user registration. It provides a secure
signup process with validation for username, email, and password
requirements.
"""

from .utils import redirect, render, User, login

def signup_process(request):
    """
    Handle new user registration process.
    
    Args:
        request (HttpRequest): The HTTP request object containing POST data
        
    Returns:
        HttpResponse: Redirects to search page on success,
                     renders signup page with errors on failure
        
    Process:
        1. Validates user input (username, email, password)
        2. Checks for existing username/email
        3. Creates new user account
        4. Automatically logs in the new user
        5. Redirects to search page
        
    Validation Rules:
        - Passwords must match
        - Email must be unique
        - Username must be unique
    """
    if request.user.is_authenticated:
        return redirect('dashboard_view') 

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation
        if password != confirm_password:
            return render(request, 'unauthed/signup/index.html', {
                'error': 'Passwords do not match'
            })

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'unauthed/signup/index.html', {
                'error': 'Email already exists'
            })

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'unauthed/signup/index.html', {
                'error': 'Username already exists'
            })

        try:
            # Create new user with hashed password
            user = User.objects.create_user(
                fullname=fullname,
                email=email,
                username=username,
                password=password
            )

            login(request, user)
            
            # Redirect to search book view
            return redirect('dashboard_view')
            
        except Exception as e:
            return render(request, 'unauthed/signup/index.html', {
                'error': 'An error occurred during signup. Please try again.'
            })

    return render(request, 'unauthed/signup/index.html')
