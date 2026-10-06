# Issue fix history

## Overview

This document records the main issue categories encountered while building and securing the custom email-based Django authentication project.

## 1. Authentication and custom model setup

Issue:
- username-based flow conflicted with email-based login requirements

Fix:
- custom `CustomUser` model set email as username field
- custom backend added to authenticate by email and password

## 2. Dashboard and role restrictions

Issue:
- incorrect role logic blocked valid users and made 403 errors appear

Fix:
- dashboard access moved to staff/admin only
- members were redirected away from the dashboard

## 3. URL and redirect errors

Issue:
- stale route names and circular import risks caused broken redirects

Fix:
- use consistent namespaced routes
- avoid resolving lazy URLs during module import startup

## 4. Security configuration

Issue:
- project secrets and SMTP config were not production-safe

Fix:
- `.env` support added
- `ALLOWED_HOSTS`, secrets, and email config placed under environment variables

## 5. Email delivery

Issue:
- signup and password reset email flow was incomplete or not validated

Fix:
- welcome email and reset email flow were integrated and tested

## 6. Editor / static analyzer warnings

Issue:
- Pyright and Pylance repeatedly reported warnings that looked like code problems

Fix:
- model annotations cleaned up
- custom manager cast added in the demo command
- workspace Pyright config added

## 7. Deployment risk notes

Issue:
- local app setup was stable, but production deployment was not yet configured

Fix:
- documented deployment plan using Docker + PostgreSQL + Gunicorn + Nginx
- recommended managed hosting as a simpler first deployment option
