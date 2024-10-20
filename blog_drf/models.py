# blog_drf/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    """Custom manager for the User model."""

    def create_user(self, username, email, password=None):
        """Creates and returns a user with a specified username and email."""
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        
        # Check if the username is unique
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """Creates and returns a superuser."""
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User model."""
    
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self) -> str:
        """Returns the username as a string."""
        return str(self.username)
