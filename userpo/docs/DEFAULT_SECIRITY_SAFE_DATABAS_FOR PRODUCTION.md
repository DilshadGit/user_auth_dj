# DEFAULT SECURITY SAFE DATABASE FOR PRODUCTION

This is the required pre-deployment security checklist. Read it before every production deployment.

---

## 1. Required rules

- Do not expose DEBUG mode in production.
- Use environment variables for all secrets and database settings.
- Use PostgreSQL in production, not SQLite.
- Keep HTTPS enabled with a valid certificate.
- Run Django behind Gunicorn with Nginx in front.
- Keep user records and audit history permanently unless there is a legal or policy reason to archive them.
- Never delete active user records permanently from the database.
- Enforce inactive and deleted-user blocking during authentication.
- Keep email reset and password flows secure and verified.

---

## 2. Data preservation rule

The system must preserve history. Do not hard-delete user records when a user is removed from the active system. Prefer soft-delete patterns and audit logs so that:

- account history remains available
- changes remain traceable
- compliance and investigations remain possible
- production recovery is safer

---

## 3. Auth security rule

- use the custom user model with email-based authentication
- keep all login logic in view classes and forms
- validate login, signup, and reset forms strictly
- block inactive or deleted users from login
- restrict dashboard access to staff/admin users only
- keep all role checks server-side in the view logic

---

## 4. Production deployment readiness

Before any production release, confirm the following:

1. env values are correct for the live server
2. database is PostgreSQL and reachable
3. Django checks pass
4. tests pass
5. SMTP is configured with a trusted provider
6. reset links use the real domain
7. admins require strong MFA or equivalent protections
8. Nginx and Gunicorn are running correctly
9. HTTP requests are redirected to HTTPS
10. error logs and access logs are enabled
11. secrets are not committed to git history
12. backups are enabled and tested

---

## 5. Operational safety policy

If any production problem appears:

- do not continue blindly
- stop deployment if auth or recovery flows are broken
- inspect Django, Nginx, and Gunicorn logs
- fix root cause before redeploying
- preserve database history while troubleshooting

---

## 6. Final recommendation

The project should remain in a secure, audited, and minimal-disruption pattern:

- Django custom auth flow
- role-based access control
- audit logs for profile changes
- soft-delete users rather than hard-delete
- environment-variable secrets
- production deployment checklist before every release

This is the safest and most professional pattern for a live system.
