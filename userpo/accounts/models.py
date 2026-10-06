# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('An email address is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    # def create_superuser(self, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # Remove the username field
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='accounts_user_set',
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     verbose_name='groups',
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='accounts_user_permission_set',
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions',
    # )
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email