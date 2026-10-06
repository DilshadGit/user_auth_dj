# Missing Items and Next Steps

This list captures the important items still missing before the project is fully production-grade and safer for real-world deployment.

## 1. Production email delivery

Still needed:
- configure a real transactional email provider such as Gmail App Password, Mailgun, SendGrid, or Postmark
- store real SMTP credentials in the environment only
- confirm sending works from a clean production or staging setup
- add domain-based sender validation to reduce spam risk

Why this matters:
- the app can send email in development mode, but a production-quality service is needed before live use

## 2. Email verification on signup

Still needed:
- verify email address on first signup
- add a confirmation token and verification page
- prevent full access until email is verified
- allow the user to request a resend if needed

This is important if you want stronger identity control and fewer fake accounts.

## 3. Stronger account lockout and brute-force protection

Still needed:
- lock out or throttle repeated failed login attempts
- log login failures by IP and email
- optionally notify admins for suspicious failed-login patterns

The project already includes django-axes, but the rules and monitoring should be tuned to your real environment.

## 4. Multi-factor authentication (MFA)

Still needed:
- optional 2FA or MFA for staff/admin accounts
- backup codes or recovery flow
- admin-only MFA requirement if the project is used in a sensitive environment

This is especially recommended for admin and staff-level user accounts.

## 5. Deployment and hosting hardening

Still needed:
- deploy behind HTTPS with a proper domain
- set DEBUG = False in production
- configure trusted hosts correctly
- enable a real database for production instead of local SQLite
- set up file storage for media in a production-safe location
- configure backups and retention policy

## 6. Role policy cleanup and policy documentation

Still needed:
- document precise permission rules for admin, staff, and member roles
- define which users can view, edit, delete, and export data
- review the current access model for any edge cases in role escalation

## 7. Audit and compliance review

Still needed:
- review all admin actions and audit log coverage
- add policy entries for data retention and deletion behavior
- document how user records are archived and soft-deleted
- define who can access identity data like barcode, DOB, address, and mobile number

## 8. Privacy and security review

Still needed:
- confirm data minimization rules for personal data exposure
- review which fields are visible to staff versus admin only
- define the exact policy for blocked or suspended users
- confirm user profile image permissions are appropriate

## 9. Backup, restore, and incident response

Still needed:
- database backup automation
- restore verification process
- incident response documentation for compromised accounts
- admin notification procedure for suspicious activities

## 10. Final quality checklist before production release

Still needed before launch:
- production environment variables verified
- real SMTP credentials tested
- admin account recovery plan documented
- role access testing completed
- user blocking and unblocking flow reviewed
- password reset and verification emails tested end-to-end
- user profile image uploads tested in production storage
- dashboard search and user listing reviewed with real data

## Final summary

The project is already far along and the core system is working well, but it is not yet completely production-ready. The biggest missing items are:
- real email service for production
- email verification for new users
- stronger login protection and MFA
- production deployment hardening
- formal audit and privacy review

Once these are addressed, the application will be much safer and more suitable for real-world deployment.
