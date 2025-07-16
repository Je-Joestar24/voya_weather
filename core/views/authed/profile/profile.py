"""
Profile View Module
-------------------
Handles user profile management, including displaying and updating user information for authenticated users.
"""

from core.views.authed.util import render, messages, login_required

@login_required
def profile_view(request):
    """
    Handle user profile display and updates for authenticated users.
    Args:
        request (HttpRequest): The HTTP request object containing POST data for updates.
    Returns:
        HttpResponse: Renders the profile page with user data and status messages.
    Process:
        GET: Displays current user profile information.
        POST: Updates user profile, handles validation, and provides feedback.
    Context Data:
        fullname, username, email, id, status, message
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