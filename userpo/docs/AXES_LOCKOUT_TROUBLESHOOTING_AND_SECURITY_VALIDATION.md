# AXES Lockout Troubleshooting and Security Validation

This document explains why the account lockout message appears, how it was resolved, and the final security validation that confirmed the project data was still intact.

---

## 1. Why the lockout message appears

The project uses django-axes for failed-login protection. The lockout is triggered by repeated invalid login attempts and is intentional security behavior.

The relevant app settings are configured in `userpo/config/settings.py` and include:

- `axes` in `INSTALLED_APPS`
- `axes.middleware.AxesMiddleware`
- `axes.backends.AxesStandaloneBackend`

When a user enters the wrong password too many times, django-axes records the failed attempts and blocks future logins. The resulting message is:

> Account locked: too many login attempts. Contact an admin to unlock your account.

This is not a sign that the user has been deleted or that the database has lost records.

---

## 2. Root cause

The most common cause is repeated failed login attempts due to:

- incorrect password entry
- browser auto-fill or stale test attempts
- repeated trial attempts while debugging login behavior
- a user being locked by brute-force protection after several failed logins

The system is intentionally designed to protect against brute-force attacks, which is why the lockout happens.

---

## 3. What was done to reduce lockout impact for local testing

The lockout threshold was tuned for a safer local environment while keeping security active.

The final settings used are:

- `AXES_FAILURE_LIMIT = 8`
- `AXES_COOLOFF_TIME = timedelta(minutes=30)`
- `AXES_RESET_ON_SUCCESS = True`
- `AXES_LOCKOUT_PARAMETERS = ["username"]`

This keeps the protection active but avoids overly aggressive lockouts during routine local testing.

---

## 4. How to unlock the account

To clear accumulated failed attempts and reset lockouts, run:

```bash
cd /home/monika/PycharmProjects/Devel/user_auth_dj/userpo
../.venv/us/bin/python manage.py axes_reset
```

This command was verified to exist in the installed django-axes version used by the project.

---

## 5. Verified database state

After resetting lockout records and running validation, the database was checked directly.

Verified results:

- Total users: 100
- Admins: 2
- Staff: 4
- Members: 94
- Deleted users: 0
- Inactive users: 0

This confirms the full dataset remained intact and nothing was deleted from the database.

The admin emails still present are:

- dilshad.a73@gmail.com
- dilshad.abdulla@icloud.com

---

## 6. Final validation evidence

I ran the following checks successfully:

```bash
cd /home/monika/PycharmProjects/Devel/user_auth_dj/userpo
../.venv/us/bin/python manage.py axes_reset
../.venv/us/bin/python manage.py check
../.venv/us/bin/python manage.py test accounts
```

Result:

- System check identified no issues (0 silenced)
- Ran 12 tests in 8.692s
- OK

This confirms the project remains secure, the auth configuration passes Django checks, and the user records remain intact.

---

## 7. Security recommendation

For production, keep the brute-force protection enabled. For local testing, tune the threshold to match real use. The safe pattern is:

- keep django-axes enabled
- limit lockout severity for testing
- reset failed attempts after successful login
- preserve historical user records
- keep sensitive user data protected by Django's secure auth system

This follows the production-safe principles in the project checklist and keeps the project consistent with a professional deployment approach.
