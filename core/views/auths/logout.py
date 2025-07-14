"""
Logout View Module

This module handles user logout functionality. It ensures that only
authenticated users can access the logout process and properly
terminates their session.
"""

from .utils import login_required, logout, redirect

@login_required
def logout_process(request):
    """
    Handle user logout process.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Redirects to home page after successful logout
        
    Note:
        This view is protected by the @login_required decorator to ensure
        only authenticated users can access it.
    """
    logout(request)
    return redirect('home_view')