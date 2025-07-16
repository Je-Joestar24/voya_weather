"""
Signup View Module
------------------
Handles new user registration using Django's form system for validation and model binding.
"""

from .utils import redirect, render, User, login, messages
from django import forms

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["fullname", "email", "username", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username


def signup_process(request):
    """
    Handle new user registration process using Django's form system.
    Args:
        request (HttpRequest): The HTTP request object containing POST data
    Returns:
        HttpResponse: Redirects to dashboard on success, renders signup page with errors on failure
    """
    if request.user.is_authenticated:
        return redirect('dashboard_view')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                fullname=form.cleaned_data['fullname'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, "Signup successful! Welcome to VoyaWeather.")
            return redirect('dashboard_view')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, 'unauthed/signup/index.html', {'form': form})
