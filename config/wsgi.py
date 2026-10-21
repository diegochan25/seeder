import os
from django.core.wsgi import get_wsgi_application

django_settings_module = ''

match (os.environ.get('PYTHON_ENV', 'development')):
    case 'production':
        django_settings_module = 'config.settings.production'
    case 'development':
        django_settings_module = 'config.settings.development'
    case _:
        django_settings_module = 'config.settings.base'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings_module)

application = get_wsgi_application()
