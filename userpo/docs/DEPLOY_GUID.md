# Production Deployment and Hardening Guide

This guide follows the correct deployment order for this project:

1. Real SMTP and tested signup/reset emails
2. Email verification before activation
3. CAPTCHA + honeypot + signup rate limiting
4. PostgreSQL in production
5. HTTPS deployment with Gunicorn and Nginx

The project already works in development mode. The remaining work is production hardening and deployment preparation.

---

## 1. Configure real SMTP first

Before moving to production, the app must send real transactional emails successfully.

### 1.1 Choose an SMTP provider

Recommended providers:

- Resend
- Mailgun
- SendGrid
- Postmark

Use a dedicated sender address such as:

- no-reply@yourdomain.com
- support@yourdomain.com

### 1.2 Add real email settings to the environment

Use these values in the production `.env` file:

```env
DJANGO_DEBUG=0
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your-smtp-user
EMAIL_HOST_PASSWORD=your-smtp-password
DEFAULT_FROM_EMAIL=no-reply@yourdomain.com
SERVER_EMAIL=no-reply@yourdomain.com
```

### 1.3 Test real emails

Run a smoke test from the Django shell:

```bash
python manage.py shell -c "from django.core import mail; mail.send_mail('Test subject', 'This is a test email.', 'no-reply@yourdomain.com', ['you@example.com'])"
```

Then verify:

- signup email works
- password reset email works
- reset link loads correctly
- sender address matches your domain
- no email is being sent to an invalid or blacklisted address

### 1.4 Confirm the reset flow is live

Check these pages in production:

- `/accounts/signup/`
- `/accounts/password_reset/`
- `/accounts/password_reset_confirm/.../`

Make sure links sent by email point to the correct host and domain.

---

## 2. Add email verification before activation

This is the next security step after SMTP is working.

### 2.1 Required behavior

When a user signs up:

- create the account in an inactive state
- send a verification email
- require the user to click the link before the account becomes active

### 2.2 Recommended model field

Add a field such as:

```python
email_verified = models.BooleanField(default=False)
email_verification_token = models.CharField(max_length=255, blank=True, null=True)
email_verification_sent_at = models.DateTimeField(blank=True, null=True)
```

### 2.3 Recommended flow

1. User signs up
2. System creates account with `is_active = False`
3. Django sends verification email
4. User clicks tokenized link
5. System sets `email_verified = True` and `is_active = True`
6. User can log in normally

### 2.4 Why this matters

This prevents fake accounts and stops bots from creating active users without real email confirmation.

---

## 3. Add CAPTCHA, honeypot, and rate limiting

This is the best anti-bot protection layer.

### 3.1 Use CAPTCHA

Recommended choices:

- hCaptcha
- Google reCAPTCHA
- Cloudflare Turnstile

Best practice:

- require CAPTCHA on signup
- optionally require it on password reset forms if spam risk is high

### 3.2 Add a honeypot field

Add a hidden field to the signup form that is not shown to users:

```python
honeypot = forms.CharField(required=False, widget=forms.HiddenInput())
```

Then reject the request if the hidden field contains data.

### 3.3 Add rate limiting

Use either:

- `django-ratelimit`
- `django-axes`
- nginx rate limiting as a second layer

Recommended thresholds:

- no more than 5 signup attempts per IP per 10 minutes
- no more than 3 password reset requests per email per hour
- block repeated attempts after a threshold is reached

### 3.4 Block disposable email domains

Reject common temporary email providers such as:

- mailinator.com
- tempmail.com
- 10minutemail.com
- throwawaymail.com

This can be done with a simple blocklist in the signup validation layer.

---

## 4. Move to PostgreSQL for production

SQLite is fine for development, but PostgreSQL is the correct production database.

### 4.1 Install PostgreSQL dependencies

```bash
pip install psycopg[binary]
```

### 4.2 Create a production database

Example:

```sql
CREATE DATABASE app_db;
CREATE USER app_user WITH PASSWORD 'strong-password';
ALTER ROLE app_user SET client_encoding TO 'utf8';
ALTER ROLE app_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE app_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE app_db TO app_user;
```

### 4.3 Add PostgreSQL environment variables

```env
POSTGRES_DB=app_db
POSTGRES_USER=app_user
POSTGRES_PASSWORD=strong-password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

### 4.4 Update Django settings

Use a production config like this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'app_db'),
        'USER': os.environ.get('POSTGRES_USER', 'app_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'change-me'),
        'HOST': os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}
```

### 4.5 Run migrations and collect static files

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## 5. Deploy behind HTTPS with Gunicorn + Nginx

This is the production web stack.

### 5.1 Install Gunicorn

```bash
pip install gunicorn
```

### 5.2 Create a Gunicorn service

Example service command:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

For a systemd service, create a unit file and enable it.

### 5.3 Configure Nginx as a reverse proxy

Example Nginx config:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }

    location /static/ {
        alias /path/to/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/project/media/;
    }
}
```

### 5.4 Enable HTTPS

Use Certbot:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 5.5 Force secure settings

Make sure this is enabled in production:

```python
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## 6. Final production verification checklist

Before going live, confirm the following:

- SMTP is configured with a real provider
- signup emails are delivered successfully
- reset emails are delivered successfully
- email verification is enforced before login
- CAPTCHA is active on signup
- honeypot field rejects bot traffic
- signup rate limiting blocks abuse
- PostgreSQL is the database in production
- Gunicorn is serving the app
- Nginx is terminating HTTPS correctly
- production secrets are stored in environment variables only
- `DEBUG` is `False`
- admin and staff accounts are protected with MFA

---

## 7. Recommended validation commands

Run these before production launch:

```bash
python manage.py check
python manage.py test accounts
python manage.py migrate
python manage.py collectstatic --noinput
```

Then do a live smoke test:

- create an account
- confirm the verification email arrives
- click the verification link
- log in successfully
- request a password reset
- confirm the email arrives
- confirm dashboard access rules work

---

## 8. Final recommendation

The app is already working well in development. The correct final production path is:

1. SMTP working with real email delivery
2. email verification before activation
3. CAPTCHA + honeypot + rate limiting
4. PostgreSQL in production
5. HTTPS via Nginx + Gunicorn

This is the safest and cleanest path for a secure public deployment.
