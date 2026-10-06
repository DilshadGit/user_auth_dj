Django 5.2 User Authentication — Zero to Hero (Complete Guide)
Django 5.2 (LTS) already includes a production-ready authentication system (django.contrib.auth). You get users, groups, permissions, password hashing (PBKDF2 by default), sessions, and ready-made views/forms.

1. Project Setup (From Zero)
Bash# Create virtual environment
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

# Install Django 5.2
pip install Django==5.2.*

# Create project
django-admin startproject config .
python manage.py startapp accounts

# config/settings.py — make sure these are present (they are by default):
PythonINSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',          # ← required
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',                     # your app
]

MIDDLEWARE = [
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ← required
    # ...
]

LOGIN_REDIRECT_URL = '/'          # after successful login
LOGOUT_REDIRECT_URL = '/'         # after logout
LOGIN_URL = 'login'               # where @login_required sends users

Run migrations:
Bashpython manage.py migrate
python manage.py createsuperuser

2. Custom User Model (Strongly Recommended)
Do this before the first migration if possible.
accounts/models.py
Pythonfrom django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add extra fields if you want
    bio = models.TextField(blank=True)
    # email is already unique in AbstractUser in modern Django

    def __str__(self):
        return self.username
config/settings.py
PythonAUTH_USER_MODEL = 'accounts.User'
Then:
Bashpython manage.py makemigrations
python manage.py migrate

3. Built-in Auth Views (Easiest Way)
Django already provides login, logout, password change, and password reset views.
config/urls.py
Pythonfrom django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # magic!
    # or include your own app urls
    path('', include('accounts.urls')),
]

# This automatically gives you:

# URL                                Name                        Purpose
/accounts/login/                login                       Login
/accounts/logout/               logout                      Logout
/accounts/password_change/      password_change             Change password
/accounts/password_reset/       password_reset              Request reset 

email... and confirmation / done pages

4. Templates (Required)
Create these files under templates/registration/:
texttemplates/
└── registration/
    ├── login.html
    ├── password_reset_form.html
    ├── password_reset_done.html
    ├── password_reset_confirm.html
    ├── password_reset_complete.html
    └── password_change_form.html

# Example login.html
HTML

{% extends "base.html" %}
{% block content %}
<h2>Login</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Login</button>
</form>
<p><a href="{% url 'password_reset' %}">Forgot password?</a></p>
{% endblock %}

# Base template tip — show username and logout:
HTML
{% if user.is_authenticated %}
  Hello {{ user.username }}!
  <form action="{% url 'logout' %}" method="post">
    {% csrf_token %}
    <button type="submit">Logout</button>
  </form>
{% else %}
  <a href="{% url 'login' %}">Login</a>
{% endif %}

5. Custom Registration (Sign-up)
# Django does not provide a built-in signup view (by design).
# accounts/forms.py
Pythonfrom django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# accounts/views.py
Pythonfrom django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# accounts/urls.py
Pythonfrom django.urls import path
from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]

# 6. Protecting Views
Pythonfrom django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def my_view(request):
    ...

class MyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

# Permissions:
Pythonfrom django.contrib.auth.decorators import permission_required

@permission_required('app.change_model')
def edit_something(request):


7. Password Reset (Email)
Add to settings.py:
PythonEMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # for development
# For production:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your@email.com'
# EMAIL_HOST_PASSWORD = 'app-password'

8. Extra Packages You Will Likely Need

Package                         Purpose                             Install command
django-allauth                  Social login (Google, 
                                GitHub…) + email verification       pip install django-allauth
django-crispy-forms + 
crispy-bootstrap5               Beautiful forms                     pip install django-crispy-forms
                                                                    crispy-bootstrap5

django-axes                     Brute-force protection              pip install django-axes

django-otp
django-two-factor-auth          2FA                                 pip install django-otp django-two-factor-auth

# Quick django-allauth setup (most popular)

# Bash
pip install django-allauth

PythonINSTALLED_APPS += [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # example
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Optional modern settings
ACCOUNT_LOGIN_METHODS = {'email'}          # or {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Add to urls.py:
# Python
path('accounts/', include('allauth.urls')),

9. Useful Commands & Tips
Bash# Create superuser
python manage.py createsuperuser

# Change password of a user
python manage.py changepassword username

# Check password validators
# settings.py already has AUTH_PASSWORD_VALIDATORS

10. Best Practices Checklist (Django 5.2)

    Always use a custom User model from day one.
    Use HTTPS in production (SECURE_SSL_REDIRECT = True).
    Set SESSION_COOKIE_SECURE = True and CSRF_COOKIE_SECURE = True.
    Use django-axes or rate limiting against brute force.
    Never store plain-text passwords (Django never does).
    Prefer class-based views + LoginRequiredMixin / PermissionRequiredMixin.
    Use get_user_model() instead of importing User directly.


# Would you like me to expand any part?

Examples:

Full project structure with templates
django-allauth complete Google login
Custom authentication backend
JWT authentication for APIs (DRF)
2FA setup

Just tell me which part you want next and I’ll give you the exact code.
