# User Authentication Django Project

A secure Django 5.2 authentication system with a custom email-based user model, role-based access control, reset flows, profile management, audit logging, and Docker-ready deployment support.

## Project overview

This project includes:

- Custom user model using email as the login field
- Sign up, login, logout, and profile management
- Password change and password reset flows
- Role-based access for admin, staff, and member users
- Dashboard access restrictions for staff/admin only
- Soft-delete-safe account handling with history preservation
- Brute-force protection with django-axes
- PostgreSQL-ready configuration with SQLite fallback for local dev
- Docker and Nginx support for local deployment
- Documentation and production safety guidance

## Key project structure

```text
user_auth_dj/
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
├── nginx/
│   └── default.conf
├── userpo/
│   ├── manage.py
│   ├── .env
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── accounts/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── backends.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── templates/
│   ├── templates/
│   └── docs/
├── media/
├── staticfiles/
└── .venv/
```

## Prerequisites

- Python 3.12+
- pip
- Virtual environment support
- Docker and Docker Compose for containerized deployment

## Local setup

From the project root:

```bash
cd /home/monika/PycharmProjects/Devel/user_auth_dj
python3 -m venv .venv/us
source .venv/us/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Then start the Django project from the app folder:

```bash
cd userpo
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

If you need a local admin user:

```bash
python manage.py createsuperuser
```

The project also includes a seeded admin account already present in the local database for validation:

- Email: dilshad.a73@gmail.com
- Password: AdminPass!2026

## Environment configuration

The app reads settings from `userpo/.env`.

Example values:

```env
DJANGO_SECRET_KEY=change-this-to-a-long-random-secret-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0,testserver

EMAIL_BACKEND=django.core.mail.backends.locmem.EmailBackend
DEFAULT_FROM_EMAIL=noreply@example.com
```

The project uses SQLite by default for local development; PostgreSQL is enabled automatically when the database environment variables are set.

## Authentication behaviour

The app uses a custom email backend and custom login form so users log in by email rather than username.

### Roles

- Admin: full dashboard and user management access
- Staff: dashboard access and restricted management permissions
- Member: profile access only

### Security features

- `django-axes` for brute-force protection
- `AXES_RESET_ON_SUCCESS = True`
- `LOGIN_URL` and protected routes enforced via `LoginRequiredMixin`
- Dashboard access restricted to staff/admin users only
- Profile updates are logged for audit review
- Soft-delete patterns keep historical data intact rather than deleting records outright

## Password and reset flows

The app includes:

- Sign up
- Login
- Logout
- Password change
- Password reset request
- Password reset confirmation
- Password reset completion

Reset emails are configured to work in local dev via console email backend before production SMTP is enabled.

## Docker workflow

From the root directory:

```bash
docker compose up --build
```

The compose file provisions:

- PostgreSQL service
- Django web service
- Nginx reverse proxy

The app is exposed on:

- Django: http://localhost:8000
- Nginx: http://localhost:8080

## Testing

Run the project tests from `userpo/`:

```bash
python manage.py test accounts
```

The app has also been validated with live Django test-client login checks against the stored admin credentials.

## Production notes

For production deployment, the project should be moved to secure configuration:

- Use PostgreSQL instead of SQLite
- Set strong secret keys and environment variables
- Restrict `ALLOWED_HOSTS`
- Turn on HTTPS and TLS
- Use production email backend and SMTP credentials
- Keep audit history and soft-delete accounting intact
- Review the docs in `userpo/docs/` before deployment

## Project documentation

Additional implementation and deployment documentation is available under:

- `userpo/docs/START_UP.md`
- `userpo/docs/PRODUCTION_AUTH_SECURITY_RECOMMENDATION_PROCESS.md`
- `userpo/docs/AXES_LOCKOUT_TROUBLESHOOTING_AND_SECURITY_VALIDATION.md`
- `userpo/docs/NGINX_GUNICORN_DOCKER_DEPLOYMENT_GUIDE.md`

## Final status

This repository delivers the requested Django authentication project as a working implementation with custom user management, secure flows, access control, audit logging, Docker support, and deployment guidance.


