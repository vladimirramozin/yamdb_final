from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, is_staff=True,
                          is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    bio = models.TextField(max_length=300, blank=True)
    confirmation_code = models.CharField(max_length=6, default='000000')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLE = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    role = models.CharField(max_length=9, choices=USER_ROLE, default='user')

    objects = CustomUserManager()

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR
