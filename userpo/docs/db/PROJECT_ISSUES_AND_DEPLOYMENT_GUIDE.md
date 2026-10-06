# Project issues summary and deployment guidance

## 1. Issue log recorded from the project

This project went through a long authentication and security hardening cycle. The main issues were not all the same type, and they were resolved in stages.

### 1.1 Custom user model and authentication mismatch

Issue:
- the app was created with a default Django user model setup, but the project later moved to an email-based custom user model
- Django still expected username-based behavior in several places

Impact:
- login and signup could fail even when the email and password were correct
- redirect names and query flow could break

Fix:
- custom `CustomUser` model was created with `USERNAME_FIELD = "email"`
- custom email authentication backend was added
- login and signup forms were aligned with the custom user model

### 1.2 URL mismatch and reverse errors

Issue:
- broken route names caused `NoReverseMatch` errors
- login/logout redirects happened to names that did not exist or were not namespaced properly

Impact:
- users were redirected incorrectly or crashed during auth actions

Fix:
- namespaced URLs were corrected
- `accounts:dashboard`, `accounts:profile`, and `accounts:login` were used consistently
- the logout redirect was changed to a safe string route instead of resolving too early during import startup

### 1.3 Session and access control problems

Issue:
- dashboard access was incorrectly restricted in ways that blocked valid users
- role checks were inconsistent with the custom user model

Impact:
- users could be blocked from valid pages or see wrong access states

Fix:
- dashboard access was limited to staff/admin only
- member users were redirected to the profile page
- validation logic was enforced in view dispatch

### 1.4 Security settings and environment variables

Issue:
- secrets and SMTP settings were stored in code or in a hard-coded default state
- project relied on unsafe defaults in development setup

Impact:
- security settings were not production-safe
- secrets could be exposed in version control

Fix:
- `.env` and `.env.example` were added
- `.gitignore` was updated to keep secrets out of the repo
- secure settings were sourced from environment variables
- headers, cookies, and session settings were hardened

### 1.5 Email sending and password reset flow

Issue:
- signup and password reset emails were not correctly aligned with the project flow
- email backend needed to be configured securely

Impact:
- recovery and registration communication could fail or be lost

Fix:
- SMTP settings were configured via environment variables
- welcome email and password reset email sending were validated through tests
- real email notification flow was confirmed through Django test suite execution

### 1.6 Pylance / editor type warnings

Issue:
- VS Code reported warnings such as `reportAttributeAccessIssue` and missing Django type metadata
- these warnings repeated in multiple files even when runtime behavior was correct

Impact:
- confusion because some warnings looked like real code problems

Fix:
- custom manager type was cast in the demo user command
- model attribute annotations were cleaned up
- workspace-level Pyright config was added
- false-positive editor warnings were documented and reduced

## 2. What was fixed successfully

The project has now been validated in its current state:

- custom email auth model works
- dashboard access is role-safe
- sign-up flow works
- login/logout works
- password reset flow works
- email notifications are covered by tests
- local validation passes with Django checks and test suite

## 3. The last important technical warning and its fix

The warning in the demo user creation command was caused by Pylance not recognizing that `get_user_model()` returns the custom app model with the custom manager attached.

The fix was to cast the result to `CustomUser` so the static type checker can see the custom `create_user()` method.

This is a typing fix only; it does not change runtime logic.

## 4. Recommended deployment strategy

For a real deployment, the best option is:

### Option A: production-grade deployment with Docker + PostgreSQL + Gunicorn + Nginx

This is the most reliable and scalable approach for Django projects.

Recommended stack:
- Django app container
- PostgreSQL database in a managed or containerized service
- Gunicorn as WSGI server
- Nginx as reverse proxy
- TLS/HTTPS termination via LetsEncrypt or a managed SSL provider
- .env-based environment variables
- static/media storage via a cloud service or mounted volumes

Benefits:
- clean production environment
- easier scaling and restarts
- better security for database and app config
- consistent deploy process

### Option B: managed hosting platform

Use a PaaS such as:
- Render
- Railway
- DigitalOcean App Platform
- Heroku (less preferred now, but workable)

Benefits:
- simpler deployment
- lower ops overhead
- easier for small teams

For this project, a managed Django host is a good option if you want fast deployment without much server maintenance.

## 5. Best practice advice for your project

### Security checklist

Before production deployment, do these:
- set `DEBUG = False`
- set secret key from a real secret manager or secure env file
- restrict `ALLOWED_HOSTS`
- use HTTPS only
- configure real SMTP credentials for production
- turn on secure cookie settings in a production environment
- enforce MFA for admin/staff users
- add rate limiting and login protection
- add log reviews and admin audit trails

### Database recommendation

Use PostgreSQL in production instead of SQLite.

SQLite is fine for local development and testing, but PostgreSQL is better for:
- multi-user production apps
- safer concurrency
- better reporting and scaling
- production deployment conventions

### Static/media recommendation

Use a dedicated static/media storage strategy:
- WhiteNoise for local dev and light deployment
- object storage or CDN for production media assets

### Deployment order

Recommended sequence:
1. production environment variables configured
2. PostgreSQL database created
3. app deployed with Gunicorn
4. reverse proxy configured
5. media/static served correctly
6. SMTP verified with real provider
7. user flows tested live
8. admin security review completed
9. backup and rollback procedure created

## 6. Final recommendation

The best deployment setup for this project is:

- Dockerized Django app
- PostgreSQL database
- Gunicorn + Nginx
- real HTTPS
- real SMTP provider
- environment-secret management
- admin MFA and review logs

If you want the simplest path to launch quickly, then:

- use a managed platform like Render or DigitalOcean App Platform
- configure PostgreSQL there
- set your .env values securely
- deploy the Django app and verify email + auth flows before exposing it to real users

## 7. Final note

This project is now in a strong working state for a secure custom-auth Django app. The remaining work is mainly deployment and production hardening, not recovery from broken authentication logic.
