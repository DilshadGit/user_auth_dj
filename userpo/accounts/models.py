# Create your models here.
import secrets
from datetime import date, datetime
from typing import ClassVar

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager["CustomUser"]):
    use_in_migrations = True

    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('An email address is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _create_user(self, email, password=None, **extra_fields):
        return self.create_user(email=email, password=password, **extra_fields)

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
    username: str = ""
    email: str
    first_name: str = ""
    last_name: str = ""
    mobile_number: str = ""
    address: str = ""
    postcode: str = ""
    last_login_ip: str | None = None
    last_logout_at: datetime | None = None
    date_of_birth: date | None = None
    barcode_number: str = ""
    profile_image: str | None = None
    is_verified: bool = True
    is_deleted: bool = False
    deleted_at: datetime | None = None
    bio: str = ""

    email = models.EmailField(unique=True)  # type: ignore[assignment]
    first_name = models.CharField(max_length=150, blank=True)  # type: ignore[assignment]
    last_name = models.CharField(max_length=150, blank=True)  # type: ignore[assignment]
    mobile_number = models.CharField(max_length=20, blank=True)  # type: ignore[assignment]
    address = models.CharField(max_length=255, blank=True)  # type: ignore[assignment]
    postcode = models.CharField(max_length=20, blank=True)  # type: ignore[assignment]
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)  # type: ignore[assignment]
    last_logout_at = models.DateTimeField(blank=True, null=True)  # type: ignore[assignment]
    date_of_birth = models.DateField(blank=True, null=True)  # type: ignore[assignment]
    barcode_number = models.CharField(max_length=80, unique=True, blank=True, default='')  # type: ignore[assignment]
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # type: ignore[assignment]
    is_verified = models.BooleanField(default=True)  # type: ignore[assignment]
    is_deleted = models.BooleanField(default=False)  # type: ignore[assignment]
    deleted_at = models.DateTimeField(blank=True, null=True)  # type: ignore[assignment]
    bio = models.TextField(blank=True)  # type: ignore[assignment]

    def generate_barcode(self):
        while True:
            barcode = f"USR-{secrets.token_hex(6).upper()}"
            if not CustomUser.objects.filter(barcode_number=barcode).exists():
                self.barcode_number = barcode
                return barcode

    def save(self, *args, **kwargs):
        if not self.barcode_number:
            self.generate_barcode()
        super().save(*args, **kwargs)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

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
    
    objects: ClassVar[CustomUserManager] = CustomUserManager()  # type: ignore[assignment]

    @property
    def role(self):
        if self.is_superuser:
            return 'admin'
        if self.is_staff:
            return 'staff'
        return 'member'

    @property
    def role_label(self):
        return {
            'admin': 'Admin',
            'staff': 'Staff',
            'member': 'Member',
        }.get(self.role, 'Member')

    def __str__(self):
        return self.email


class ProfileUpdateLog(models.Model):
    user: models.ForeignKey[CustomUser]
    field_name: str
    old_value: str = ""
    new_value: str = ""
    updated_by: str = "user"
    changed_at: datetime

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile_updates')
    field_name = models.CharField(max_length=100)  # type: ignore[assignment]
    old_value = models.TextField(blank=True, default='')  # type: ignore[assignment]
    new_value = models.TextField(blank=True, default='')  # type: ignore[assignment]
    updated_by = models.CharField(max_length=100, default='user')  # type: ignore[assignment]
    changed_at = models.DateTimeField(auto_now_add=True)  # type: ignore[assignment]

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f'{self.user.email} - {self.field_name}'