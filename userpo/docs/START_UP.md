# Django 5.2 User Authentication — Zero to Hero

Django 5.2 (LTS) includes a production-ready authentication system via `django.contrib.auth`. It gives you users, groups, permissions, password hashing, sessions, and built-in views and forms.

## 1. Project setup from zero

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

# Install Django 5.2
pip install Django==5.2.*

# Create the project and app
django-admin startproject config .
python manage.py startapp accounts
```

Then add the required settings in `config/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'
```

Run the first migrations:

```bash
python manage.py migrate
python manage.py createsuperuser
```

## 2. Custom user model

This is strongly recommended before the first migration.

`accounts/models.py`:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
```

`config/settings.py`:

```python
AUTH_USER_MODEL = 'accounts.User'
```

Then migrate:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 3. Built-in auth views

Django already gives you login, logout, password change, and password reset views.

`config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('accounts.urls')),
]
```

This automatically provides routes such as:

- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/password_change/`
- `/accounts/password_reset/`

## 4. Templates

Typical template structure:

```text
templates/
└── registration/
    ├── login.html
    ├── password_reset_form.html
    ├── password_reset_done.html
    ├── password_reset_confirm.html
    ├── password_reset_complete.html
    └── password_change_form.html
```

A basic login form example:

```html
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
```

A reusable base template pattern:

```html
{% if user.is_authenticated %}
  Hello {{ user.username }}!
  <form action="{% url 'logout' %}" method="post">
    {% csrf_token %}
    <button type="submit">Logout</button>
  </form>
{% else %}
  <a href="{% url 'login' %}">Login</a>
{% endif %}
```

## 5. Custom registration flow

Django does not provide a built-in signup view by design.

`accounts/forms.py`:

```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
```

`accounts/views.py`:

```python
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
```

`accounts/urls.py`:

```python
from django.urls import path
from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
```

## 6. Protecting views

```python
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def my_view(request):
    ...

class MyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
```

Permissions can be checked with:

```python
from django.contrib.auth.decorators import permission_required

@permission_required('app.change_model')
def edit_something(request):
    ...
```

## 7. Password reset

Add this to `settings.py` for development:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

For production, use SMTP instead:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'app-password'
```

## 8. Common package additions

| Package | Purpose | Install command |
| --- | --- | --- |
| django-allauth | Social login and account workflows | `pip install django-allauth` |
| django-crispy-forms + crispy-bootstrap5 | Better-looking forms | `pip install django-crispy-forms crispy-bootstrap5` |
| django-axes | Brute-force protection | `pip install django-axes` |
| django-otp + django-two-factor-auth | Two-factor authentication | `pip install django-otp django-two-factor-auth` |

Example `django-allauth` setup:

```python
INSTALLED_APPS += [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

## 9. Useful commands

```bash
# Create superuser
python manage.py createsuperuser

# Change a user's password
python manage.py changepassword username

# Run Django system checks
python manage.py check
```

## 10. Best practices checklist

- Always use a custom user model from day one.
- Use HTTPS in production.
- Set secure cookie settings and CSRF protections.
- Use `django-axes` or rate limiting for brute-force protection.
- Never store plain-text passwords.
- Prefer class-based views with `LoginRequiredMixin` and permission checks.
- Use `get_user_model()` instead of importing the user model directly.

## Summary

This setup gives you a secure, production-minded authentication foundation for Django 5.2. The most important pieces are the custom user model, the login flow, secure session handling, password reset, and role-based access management.
