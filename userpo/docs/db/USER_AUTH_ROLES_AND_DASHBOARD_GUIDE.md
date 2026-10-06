# User Auth, Roles, Dashboard, and Admin Setup Guide

## Overview
This document records the final authentication setup for the Django project, including the custom email-based user model, role visibility rules, protected dashboard access, seeded demo users, and secure admin account setup.

## 1. Project auth model
The project uses a custom user model with email as the username field.

Key points:
- Email is the login identifier.
- Username is removed from the custom user model.
- The custom user stores common profile details like first name, last name, and mobile number.
- Extra metadata includes login IP, logout time, verification flag, and bio.
- Passwords are stored securely through Django’s hashing system and are never stored in plain text.

Relevant files:
- accounts/models.py
- accounts/forms.py
- accounts/backends.py
- config/settings.py

## 2. Authentication flow
The auth flow includes:
- sign up
- email login
- logout
- password change
- password reset
- dashboard access

Important behavior:
- Members are not allowed to access the dashboard.
- Staff and admin users can access the dashboard.
- Login redirects staff/admins to the dashboard and members to their profile page.
- New signups are logged in immediately and redirected appropriately.

## 3. Role model
Role visibility is based on Django auth flags:

- Admin: is_superuser = True
- Staff: is_staff = True and is_superuser = False
- Member: is_staff = False and is_superuser = False

Security rule:
- Dashboard access is restricted to staff/admin only.
- Members are redirected to the profile page.

This protects the dashboard from ordinary users while keeping the app clean for standard account workflows.

## 4. Dashboard and user listing
The dashboard includes:
- user summary cards
- total user count
- admin count
- staff count
- user list table
- pagination at 20 users per page

The user list displays:
- email
- role badge
- last login
- last logout

Pagination:
- If there are more than 20 users, the table renders page controls.
- The default listing order is by newest account first.

Relevant files:
- accounts/views.py
- templates/accounts/dashboard.html

## 5. Real admin accounts
The following admin accounts were set up as secure Django admin users:

- dilshad.a73@gmail.com
- dilshad.abdulla@icloud.com

These accounts were created/updated with Django password hashing via `set_password()`, which ensures the database stores a hashed password rather than raw text.

No automatic forced reset is triggered for these users, so they remain usable unless they choose to change their passwords manually.

## 6. Demo data setup
The demo seeding command creates 100 users with the requested distribution:

- 2 admins
- 4 staff
- 94 members

This is created via the command:

```bash
python manage.py create_demo_users
```

The script ensures the user mix is exactly:
- total users = 100
- admins = 2
- staff = 4
- members = 94

Relevant file:
- accounts/management/commands/create_demo_users.py

## 7. Safe password handling
For secure database storage:
- passwords are hashed by Django before saving
- no raw password values are kept in the database
- users do not get forced reset emails unless they go through the explicit password reset flow

This approach keeps the system secure while allowing a controlled manual password change when necessary.

## 8. Important note for production
For a real production deployment, the following should be considered next:
- email verification for new accounts
- stricter rate limiting for login attempts
- audit logging for admin actions
- MFA or two-factor authentication
- environment-based secret management
- HTTPS enforcement

## 9. Validated state
The project has been validated through Django checks and account tests.

At final validation:
- total = 100
- admins = 2
- staff = 4
- members = 94
- tests passed

## 10. Summary
This project now includes:
- email-first custom auth system
- secure user model and password storage
- role-based dashboard restriction
- paginated user list
- seeded demo users
- real admin accounts for the configured emails
- safe manual password handling without forced reset unless requested
