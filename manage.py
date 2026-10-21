#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    django_settings_module = ''

    match (os.environ.get('PYTHON_ENV', 'development')):
        case 'production':
            django_settings_module = 'config.settings.production'
        case 'development':
            django_settings_module = 'config.settings.development'
        case _:
            django_settings_module = 'config.settings.base'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings_module)
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
