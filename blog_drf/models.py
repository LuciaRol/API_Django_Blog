# blog_drf/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
#from django.core.exceptions import ValidationError

class UserRole(models.TextChoices):
    """Choices for the role of a user."""
    USER = "user", "USER"
    ADMIN = "admin", "ADMIN"

class UserManager(BaseUserManager):
    """Custom manager for the User model."""

    def create_user(self, username, email, password=None, role=UserRole.USER):
        """Creates and returns a user with a specified username, email, and role."""
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)

        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, username, email, password):
        """Creates and returns an admin user."""
        user = self.create_user(username, email, password, role=UserRole.ADMIN)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """Creates and returns a superuser."""
        return self.create_admin(username, email, password)

class User(AbstractBaseUser, PermissionsMixin):
    """User model."""
    
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self) -> str:
        """Returns the username as a string."""
        return str(self.username)
    

# blog_drf/models.py



class Post(models.Model):
    """Modelo para las publicaciones de los usuarios."""
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']  # Ordena los posts de más reciente a más antiguo

    def __str__(self):
        """Devuelve el título del post como una representación en cadena."""
        return self.title


