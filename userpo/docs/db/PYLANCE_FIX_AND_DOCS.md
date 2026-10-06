# Pylance and Django typing cleanup

## What was fixed

The remaining issues were caused by strict editor type checking on Django model fields and by the workspace root not loading the Pyright configuration from the actual project root.

The project was updated to remove the real type issues and to keep the secure `.env` loading behavior without triggering false warnings from the `environ` stub typing.

## Actual code changes

### 1. Django model field assignments were cleaned up

The custom user model and profile log model were updated so Django field descriptors no longer trip strict type checking in the editor.

The fix used explicit model typing and targeted `# type: ignore[assignment]` comments only where Django field descriptors intentionally differ from the Python field annotation on the class.

### 2. Logout redirect typing fix

The logout view was changed to assign a resolved string value instead of a lazy URL promise:

```python
next_page: str | None = str(reverse_lazy("accounts:login"))
```

This avoids the static type mismatch while preserving the same redirect behavior.

### 3. Correct workspace-level Pyright setup

A project-level config was placed at the workspace root:

- /home/monika/PycharmProjects/Devel/user_auth_dj/pyrightconfig.json

This ensures the editor uses the correct venv and suppresses the noisy missing-import warnings for packages already installed in the actual project environment.

### 4. `environ` usage was converted to the safer `os.environ.get` pattern

The `.env` file is still being loaded with `environ.Env().read_env(...)`, but the app values are read through `os.environ.get(...)` so the project stays secure and avoids the strict typing overloads from the `environ` stub definitions.

## Why this happened

The main issue was not a broken Django logic flow. It was a static analysis problem caused by:

- Django model fields being descriptors rather than plain Python values
- Pylance strict checks on annotations
- the static checker not being pointed at the actual workspace root
- the `environ` package typing stubs not working cleanly with keyword defaults

## Result

The project has a stable, working auth setup and the editor noise was reduced to the real project configuration baseline.

The app was also validated again with Django runtime checks and the project test suite to confirm the cleanup did not change behavior.
