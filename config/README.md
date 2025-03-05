# Configuration Folder

This `config` folder serves as the centralized location for managing all configurations and environment variables required by the project. By keeping all configurations in one place, we ensure consistency, maintainability, and clarity when working with environment-dependent settings.

## Structure

The folder contains the following files:

### 1. `celery.py`
- Defines and initializes the **Celery server**.
- Centralized setup for asynchronous task execution.
- Ensures that Celery workers have a consistent configuration across the project.

### 2. `settings.py`
- Loads **all** environment variables from the `.env` file.
- Acts as the single source of truth for configuration values.
- Any module requiring environment variables should retrieve them from `settings.py` instead of loading them separately.

## Usage Guidelines

- **Single Source of Truth:** All environment variables should be defined and accessed only via `settings.py`. This avoids unexpected or scattered imports of environment variables throughout the codebase.
- **Modular and Scalable:** As the project grows, additional configuration files can be added to this folder to keep different services organized.
- **Easy Extraction:** If a specific module is extracted from the project, the required environment variables can be easily identified in `settings.py`.

## Future Expansion

As the project scales, the `config` folder may include:
- Database configuration files
- Logging settings
- Caching configurations (e.g., Redis, Memcached)
- Third-party service credentials

By maintaining a structured and centralized configuration management approach, we ensure the project remains **organized, scalable, and easy to maintain**.
