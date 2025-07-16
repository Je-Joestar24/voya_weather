"""
Login View Module
-----------------
Handles user authentication using Django's form system for validation and user authentication.
"""

from .utils import render, redirect, User, authenticate, login, messages
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username_or_email and password:
            # Try to authenticate with username
            user = authenticate(None, username=username_or_email, password=password)
            if user is None:
                # Try to authenticate with email
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(None, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            if user is None:
                raise forms.ValidationError("Invalid username/email or password")
            self.user = user
        return cleaned_data


def login_process(request):
    """
    Handle user login process using Django's form system.
    Args:
        request (HttpRequest): The HTTP request object containing POST data
    Returns:
        HttpResponse: Redirects to dashboard on success, renders login page with errors on failure
    """
    if request.user.is_authenticated:
        return redirect('dashboard_view')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            next_url = request.GET.get('next', '/dashboard/')
            messages.success(request, "Login successful! Welcome back.")
            return redirect(next_url)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'unauthed/login/index.html', {'form': form})