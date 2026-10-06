# Authentication and Security Work Process

This document records the work completed to build, fix, and harden the Django authentication system for this project. It includes the setup process, bug fixes, UI improvements, security hardening, and the packages used in the project.

## 1. Project objective
The project was created to support a secure user authentication flow with:

- custom user model support
- email-based login
- sign-up and account registration
- profile access
- password change and reset
- secure login/logout flow
- admin-style dashboard navigation
- production-minded security settings for a protected application

## 2. Core project structure used
The active project lives under:

- /home/monika/PycharmProjects/Devel/user_auth_dj/userpo

Core files involved in the work:

- accounts/models.py
- accounts/forms.py
- accounts/views.py
- accounts/urls.py
- accounts/backends.py
- config/settings.py
- config/urls.py
- templates/navbar.html
- templates/accounts/*.html
- static/css/auth.css

## 3. Authentication setup and fixes completed

### 3.1 Custom user model
A custom user model was configured so authentication is based on email rather than a username.

Implemented elements:

- custom `CustomUser` model in `accounts/models.py`
- `USERNAME_FIELD = "email"`
- unique email requirement
- custom manager for user creation
- proper `AUTH_USER_MODEL = 'accounts.CustomUser'`

This was necessary because the default Django auth model expects a username field unless explicitly changed.

### 3.2 Email login support
The app originally had a mismatch between:

- the form expecting email
- Django using username-based authentication

This caused successful email/password combinations to fail even when credentials were correct.

The fix included:

- creating a custom email backend in `accounts/backends.py`
- using `authenticate(request, email=email, password=password)`
- updating the login form to collect email input and validate it properly
- adding the custom backend to `AUTHENTICATION_BACKENDS`

### 3.3 Sign up flow
The registration form was completed and aligned with the custom email user model.

Included work:

- `SignUpForm` for email/password signup
- custom user creation flow
- login after successful registration
- redirect to dashboard after sign-up

### 3.4 Login/logout route fixes
Multiple issues appeared during setup, including stale URL names and route mismatches.

Fixes included:

- correcting namespaced redirects like `accounts:dashboard`
- fixing broken login and signup URL mappings
- preventing `NoReverseMatch` errors when redirecting after login or signup
- custom logout view so GET renders the confirmation page and POST performs the actual logout without a 405 error

### 3.5 Dashboard access and user status flow
A 403 issue appeared because the app was blocking users based on an `is_verified` flag that was defaulted to `False` and no real email verification flow existed.

The project was adjusted to:

- allow authenticated users through the dashboard during development
- keep the app functional while no full email verification system is implemented yet
- avoid blocking valid users before verification is added

## 4. User interface improvements completed

### 4.1 Navbar layout
The top navigation was redesigned to be cleaner and more practical for an account-based application.

Included changes:

- centered navigation layout
- clear account area
- email shown in the account dropdown
- quick links under the email for:
  - View profile
  - Change password
  - Logout

### 4.2 Dashboard page styling
A minimal CMS/dashboard layout was added to keep the page professional and usable.

Included improvements:

- clean welcome section
- account summary card
- simple and readable layout
- no duplicate action buttons in the main dashboard body

### 4.3 Shared account page styling
The profile and account management pages were standardized to the same visual style so the user experience feels consistent across:

- profile page
- password change page
- password reset pages
- password reset confirmation pages
- logout page

### 4.4 Footer update
The previous footer placeholder was replaced with a proper simple footer that explains the product purpose and keeps the layout polished.

## 5. Security hardening completed

The project was hardened for a more serious production-ready baseline, which is especially relevant for sensitive apps such as hospital systems or camera/security systems.

### Added security improvements

- secure secret key source via environment variable
- debug flag controlled by environment variable
- allowed hosts controlled by environment variable
- stronger password minimum length (12)
- secure cookie configuration:
  - `SESSION_COOKIE_HTTPONLY = True`
  - `SESSION_COOKIE_SAMESITE = 'Lax'`
  - `CSRF_COOKIE_HTTPONLY = True`
  - `SESSION_COOKIE_SECURE = not DEBUG`
  - `CSRF_COOKIE_SECURE = not DEBUG`
- session hardening:
  - session expiry
  - browser-close expiry
  - session lifetime defined
- HTTP security headers:
  - `SECURE_CONTENT_TYPE_NOSNIFF = True`
  - `SECURE_BROWSER_XSS_FILTER = True`
  - `SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'`
  - `X_FRAME_OPTIONS = 'DENY'`
- HTTPS protection:
  - `SECURE_SSL_REDIRECT = not DEBUG`
  - HSTS settings enabled in production
- proxy SSL header support for reverse-proxy deployment

### Security test coverage
A minimal security test suite was created in `accounts/tests.py` to ensure the important protections remain in place.

## 6. Packages used in the project
The following packages are installed and referenced in the project.

```text
asgiref==3.12.1
certifi==2026.7.22
charset-normalizer==3.5.2
crispy-bootstrap5==2026.9
Django==5.2.17
django-allauth==65.19.7
django-crispy-forms==2.7
django-formtools==2.7
django-otp==1.7.3
django-phonenumber-field==8.5.0
django-two-factor-auth==1.18.1
idna==3.20
qrcode==8.2
requests==2.34.2
sqlparse==3.6.0
urllib3==2.8.0
```

Notes:

- Django is the main framework used.
- `django-allauth` was included for possible social login support.
- `django-crispy-forms` and `crispy-bootstrap5` were added to support nicer forms.
- `django-two-factor-auth`, `django-otp`, and related packages are present and may be useful for stronger authentication if the project is expanded into a real high-security environment.

## 7. Validation completed
The project was checked repeatedly during development and after major changes.

Validation commands used:

- `python manage.py check`
- `python manage.py test accounts`
- `python manage.py shell` reverse URL checks

The last validation confirmed:

- Django system checks passed
- account route resolution passed
- security tests passed

## 8. Recommended next steps for production security
For a real hospital, medical system, or speed camera/security platform, the next recommended improvements are:

1. email verification for new accounts
2. two-factor authentication (2FA)
3. rate limiting on login attempts
4. audit logging for all authentication actions
5. database file encryption and secure storage for sensitive records
6. HTTPS-only deployment behind a reverse proxy or application gateway
7. server hardening and role-based access control
8. separate admin and user role permissions
9. secret management with environment variables or a secret manager
10. regular dependency updates and scanning

## 9. Summary
This project was brought from a broken or partially configured Django auth setup into a more complete and secure user authentication system. The main accomplishments were:

- custom email-based user model
- email login support
- signup and account management flow
- password change/reset support
- fixed login/logout redirect and method issues
- modern dashboard and account page layout
- stronger default security settings for a protected environment

This gives a usable base for a serious production application while still leaving room for the stronger enterprise security features that high-assurance systems require.
