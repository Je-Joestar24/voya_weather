"""
Profile View Module
-------------------
Handles user profile management, including displaying and updating user information for authenticated users.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Handle user profile display and updates for authenticated users.
    Supports GET (display) and POST (update) requests.
    Inherits from Django's TemplateView and requires authentication.
    """
    template_name = 'authed/profile/index.html'

    def get_context_data(self, **kwargs):
        """
        Build context for the profile page, including user data and status messages.
        Returns:
            dict: Context for template rendering.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'fullname': user.fullname,
            'username': user.username,
            'email': user.email,
            'id': user.id,
            'status': 'info',
            'message': 'PROFILE PAGE',
        })
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle profile update via POST request. Updates user fields and provides feedback.
        Args:
            request (HttpRequest): The HTTP request object containing POST data for updates.
        Returns:
            HttpResponse: Renders the profile page with updated user data and status messages.
        """
        user = request.user
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        try:
            user.fullname = fullname
            user.email = email
            user.username = username
            user.save()
            messages.success(request, 'Profile updated successfully')
            status = 'success'
            message = 'PROFILE UPDATED'
        except Exception as e:
            messages.error(request, str(e))
            status = 'error'
            message = str(e)
        context = self.get_context_data()
        context.update({
            'status': status,
            'message': message,
        })
        return self.render_to_response(context)