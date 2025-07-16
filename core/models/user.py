"""
Custom User Model
-----------------
Defines the custom User model for VoyaWeather, including authentication, profile fields, and timestamps.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    """
    Custom manager for User model.
    Provides methods to create regular users and superusers.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The username must be set.")
        if not email:
            raise ValueError("The email must be set.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)          # ← hashed automatically
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given username, email, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for authentication and profile data.
    Fields:
        username: Unique username
        email: Unique email address
        fullname: Optional full name
        is_active: Account active status
        is_staff: Admin/staff status
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    username    = models.CharField(max_length=150, unique=True)
    email       = models.EmailField(unique=True)
    fullname   = models.CharField(max_length=255, blank=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(default=timezone.now, editable=False)
    updated_at  = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        """String representation: username"""
        return self.username
