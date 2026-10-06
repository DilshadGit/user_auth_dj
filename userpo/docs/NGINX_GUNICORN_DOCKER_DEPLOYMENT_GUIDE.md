# Nginx, Gunicorn, and Docker Deployment Guide

This guide explains how the project is deployed using Docker, Gunicorn, and Nginx, and why each component is used in the stack.

---

## 1. Overview

The project runs in a production-style stack with three main layers:

1. Nginx - receives real HTTP traffic and forwards it to Django
2. Gunicorn - runs the Django application in production mode
3. Docker - packages the app and its dependencies so it can run consistently in any environment

This setup is more stable and closer to a real production deployment than running Django with the built-in development server.

---

## 2. Why use Nginx?

Nginx acts as the front door for the application.

It is responsible for:

- receiving incoming web requests
- serving static files efficiently
- forwarding requests to Gunicorn
- handling traffic and reducing load on the app server
- improving performance and reliability

In this project, Nginx sits in front of Django and acts as the HTTP server. Traffic from the browser reaches Nginx first, and Nginx then passes the request to Gunicorn.

---

## 3. Why use Gunicorn?

Gunicorn is the WSGI server that runs Django in production.

It is responsible for:

- starting the Django app
- managing worker processes
- handling multiple requests at the same time
- serving the application in a production-ready way

Django's built-in development server is meant only for local development. Gunicorn is much better suited for real deployment because it is designed for handling production traffic.

The project uses this command:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

This means:

- `config.wsgi:application` points to the Django WSGI app
- `0.0.0.0:8000` means accept requests on port 8000 from any network interface
- `--workers 3` starts three worker processes for better concurrency

---

## 4. Why use Docker?

Docker is used to package the application and its runtime environment in a consistent container.

Benefits of Docker:

- same app runs the same way on different machines
- dependencies are installed in one place
- easier team collaboration and deployment
- easier setup for Postgres, Nginx, and Django together

The Docker setup defines:

- the Python base image
- installed system packages
- Python dependencies
- the command to run the app

This ensures the Django application is started exactly the same every time.

---

## 5. How the stack works together

The architecture looks like this:

```text
Browser
   |
   v
Nginx
   |
   v
Gunicorn
   |
   v
Django application
   |
   v
PostgreSQL database
```

### Request flow

1. The browser sends an HTTP request to the domain or server IP.
2. Nginx receives the request.
3. Nginx forwards the request to Gunicorn.
4. Gunicorn passes the request to Django.
5. Django processes the request, loads templates, queries the database, and returns a response.
6. The response goes back through Gunicorn and Nginx to the browser.

This separation makes the stack easier to manage, more scalable, and more secure.

---

## 6. What Docker Compose does

Docker Compose is used to define and run multiple services together.

In this project, we use these services:

- `db` - PostgreSQL container
- `web` - Django + Gunicorn container
- `nginx` - Nginx container

The `docker-compose.yml` file defines how these services connect and which ports they expose.

### Example service relationship

```yaml
services:
  db:
    image: postgres:16-alpine

  web:
    build: .
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    depends_on:
      - web
```

This means:

- the web app starts after the database is available
- Nginx starts after the app is available
- they all share the same Docker network

---

## 7. Port mapping

Inside Docker, services run on their own private ports. These ports are then exposed to the host machine.

Example:

- PostgreSQL container listens on `5432`
- host machine maps it to `5433`
- Nginx container listens on `80`
- host machine maps it to `8080`

This avoids conflicts with services already running on the local machine.

Example config:

```yaml
ports:
  - "5433:5432"
```

This means:

- `5433` is the host port
- `5432` is the container port

---

## 8. Why PostgreSQL is used

PostgreSQL is used as the production database because it is:

- reliable
- scalable
- good for Django projects
- strong for production workloads

In local development, SQLite is often enough, but PostgreSQL is the correct database for production.

The project is configured to use PostgreSQL when environment variables are present:

```python
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
```

If the PostgreSQL variables are not set, Django falls back to SQLite.

---

## 9. Nginx configuration example

Nginx receives requests and forwards them to Gunicorn.

Example configuration:

```nginx
upstream userpo_backend {
    server web:8000;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://userpo_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

This means:

- Nginx listens on port 80
- it passes all traffic to the Django app running inside the web container on port 8000
- it preserves the original host and client IP information

---

## 10. The Docker build process

The Dockerfile does the following:

1. starts from a Python base image
2. installs OS dependencies
3. installs Python dependencies from `requirements.txt`
4. copies the project code into the container
5. runs database migrations and static collection
6. starts Gunicorn on port 8000

Example command inside the Dockerfile:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

That is the final app startup sequence for the container.

---

## 11. Step-by-step startup flow

When the stack is started, this is what happens:

1. Docker starts the Postgres container
2. Docker starts the Django app container
3. Django connects to PostgreSQL
4. Django runs migrations
5. Django collects static files
6. Gunicorn starts and listens on port 8000
7. Nginx starts and listens on port 8080 or 80
8. Nginx forwards browser requests to Gunicorn
9. the app responds to the browser

---

## 12. Run the stack locally

From the project root, run:

```bash
docker compose up -d --build
```

To stop it:

```bash
docker compose down
```

To view logs:

```bash
docker compose logs -f
```

To check the app from the browser:

```text
http://127.0.0.1:8080
```

---

## 13. Why this is better than development mode

Running Django with the built-in development server is fine for learning, but this stack is better for real deployment because it adds:

- stable app startup
- multiple workers
- proper HTTP front-end
- stronger production structure
- easier future scaling and hosting

---

## 14. Production note

This setup is production-ready in structure, but for public internet deployment you still need:

- HTTPS with a valid certificate
- real SMTP provider
- stronger environment secrets
- PostgreSQL credentials in production env
- `DEBUG = False`
- firewall and server hardening

---

## 15. Final summary

The stack works like this:

- Nginx receives traffic
- Gunicorn runs Django
- Docker packages the whole stack
- PostgreSQL stores the app data

This is a clean, scalable, and professional way to run a Django project in production.
